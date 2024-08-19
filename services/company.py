from sqlalchemy.orm import Session, joinedload
from database import with_db_session
from schemas.user import User
from schemas.company import Company 
from schemas.task import Task

@with_db_session
def get_companies(db: Session):
    return db.query(Company).all()

@with_db_session
def get_company_users(company_id: str, db: Session):
    return db.query(User).filter(User.company_id == company_id).all()

@with_db_session
def get_company_tasks(company_id: str, db: Session):
    company_user_ids = db.query(User.id).filter(User.company_id == company_id).subquery()
    return db.query(Task).filter(Task.created_by.in_(company_user_ids)).options(joinedload(Task.user)).all()
    
