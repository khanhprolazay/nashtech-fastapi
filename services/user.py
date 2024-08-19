from common.error import BadRequestException, NotFoundException
from schemas.user import User
from uuid import UUID
from database import with_db_session
from models.user import CreateUserDto
from passlib.context import CryptContext
from sqlalchemy.orm import joinedload, Session

brypt_context = CryptContext(schemes=["bcrypt"])

def hash_password(password: str) -> str:
    return brypt_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return brypt_context.verify(plain_password, hashed_password)

@with_db_session
def get_user_by_id(user_id: UUID, db: Session) -> User:
    return db.query(User).filter(User.id == user_id).options(joinedload(User.company)).first()

@with_db_session    
def get_users(db: Session) -> list[User]:
    return db.query(User).options(joinedload(User.company)).all()

@with_db_session
def create_user(dto: CreateUserDto, db: Session):
    exist_user = db.query(User).filter(User.email == dto.email).first() or db.query(User).filter(User.username == dto.username).first()

    if exist_user:
        raise BadRequestException()

    params = dto.dict()
    params["hashed_password"] = hash_password(params["password"])
    del params["password"]

    user = User(**params)
    db.add(user)
    db.commit()

@with_db_session
def update_company(user_id: UUID, company_id: UUID, db: Session):
    user = db.query(User).filter(User.id == user_id).first()

    if not user:
        raise NotFoundException()
    
    # If user already has a company, we should not allow to change it
    if user.company_id:
        raise BadRequestException()

    user.company_id = company_id
    db.commit()