from fastapi import APIRouter, Path, Depends, status
from models.view import UserViewModel
from common.error import NotFoundException
import services.user as service
from uuid import UUID
from services.auth import authenticate, get_user as auth_get_user, admin_guard
from database import get_session
from sqlalchemy.orm import Session
from schemas.user import User

router = APIRouter(prefix="/user", tags=["users"])

@router.get("", response_model=list[UserViewModel])
async def get_users(db: Session = Depends(get_session)):
    return service.get_users(db)

@router.get("/me", response_model=UserViewModel, dependencies=[Depends(authenticate)])
async def get_me(user: User = Depends(auth_get_user)):
    return user

@router.put("/{user_id}/company", 
            status_code=status.HTTP_204_NO_CONTENT, 
            dependencies=[Depends(authenticate), Depends(admin_guard)]
        )
async def update_company(
    user_id: UUID = Path(..., title="ID is not valid"),
    user: User = Depends(auth_get_user), 
    db: Session = Depends(get_session)
    ):
    return service.update_company(user_id, user.company.id, db)