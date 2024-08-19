from database import DBSession, get_session, with_db_session
from common.error import BadRequestException, UnauthorizedException, ForbiddenException
from schemas.user import User
from .user import verify_password, get_user_by_id
from datetime import timedelta, datetime
from environment import JWT_SECRET, JWT_ALGORITHM, JWT_REFRESH_SECRET
import jwt
from fastapi import Request, Depends
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

@with_db_session
def login(dto: OAuth2PasswordRequestForm, db: Session):
    user = db.query(User).filter(User.username == dto.username).first()

    if not user:
        raise BadRequestException()
    
    if not verify_password(dto.password, user.hashed_password):
        raise BadRequestException()
    
    access_token = create_jwt(user, JWT_SECRET, JWT_ALGORITHM, timedelta(hours=1))
    refresh_token = create_jwt(user, JWT_REFRESH_SECRET, JWT_ALGORITHM, timedelta(days=1))
    
    return { 
        'access_token': access_token,
        'refresh_token': refresh_token,
        'token_type': 'bearer'
    }
        
def create_jwt(user: User,  secret: str, algorithm: str, expries: timedelta = None):
    payload = user.to_dict()
    exprire = datetime.now() + expries if expries else datetime.now() + timedelta(minutes=10)
    payload.update({'exp': exprire})
    return jwt.encode(payload, secret, algorithm=algorithm)

def verify_jwt(token: str, secret: str, algorithm: str):
    return jwt.decode(token, secret, algorithms=[algorithm])

def refresh_token(token: str):
    try:
        payload = verify_jwt(token, JWT_REFRESH_SECRET, JWT_ALGORITHM)
        access_token = create_jwt(payload, JWT_SECRET, JWT_ALGORITHM, timedelta(minutes=10))
        return { "access_token": access_token }
    except Exception:
        raise BadRequestException()

# This function is used in dependency injection in router layer
# No need to use with_db_session decorator here
def authenticate(request: Request, token: str = Depends(oauth2_scheme), db: Session = Depends(get_session)):
    try:
        payload = verify_jwt(token, JWT_SECRET, algorithm=JWT_ALGORITHM)
        user = get_user_by_id(payload['id'], db)
        
        if not user.is_active:
            raise UnauthorizedException()
        
        request.state.user = user
    except Exception as e:
        print(e)
        raise UnauthorizedException()
    
def admin_guard(request: Request):
    user = request.state.user

    if user.company is None:
        raise ForbiddenException()
    
    if not user.is_admin:
        raise ForbiddenException()
    
def get_user(request: Request):
    return request.state.user