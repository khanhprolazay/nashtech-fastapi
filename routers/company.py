from fastapi import APIRouter, Depends
from models.view import CompanyViewModel, UserViewModel
from models.company import CompanyTaskViewModel
import services.company as service
from services.auth import authenticate, get_user, admin_guard
from schemas.user import User
from common.error import NotFoundException
from sqlalchemy.orm import Session
from database import get_session

router = APIRouter(prefix="/company", tags=["company"])

@router.get("", response_model=list[CompanyViewModel])
async def get_companies():
    return service.get_companies()

@router.get("/me", response_model=CompanyViewModel, dependencies=[Depends(authenticate)])
async def get_own_company(user: User = Depends(get_user)):
    if user.company is None:
        raise NotFoundException()
    return user.company

@router.get('/user', response_model=list[UserViewModel], dependencies=[Depends(authenticate)])
async def get_user_company(user: User = Depends(get_user), db: Session = Depends(get_session)):
    if user.company is None:
        raise NotFoundException()
    return service.get_company_users(user.company_id, db)

@router.get("/task", response_model=list[CompanyTaskViewModel], dependencies=[Depends(authenticate), Depends(admin_guard)])
async def get_company_tasks(user: User = Depends(get_user), db: Session = Depends(get_session)):
    return service.get_company_tasks(user.company_id, db)