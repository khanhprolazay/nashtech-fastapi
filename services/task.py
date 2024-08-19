from schemas.user import User
from schemas.task import Task, TaskStatus, TaskPriority
from models.task import CreateTaskDto
from sqlalchemy.orm import Session
from database import with_db_session
from common.error import NotFoundException, ForbiddenException

@with_db_session
def create_task(user: User, dto: CreateTaskDto, db: Session):
    params = dto.dict()
    params.update({"created_by": user.id})
    task = Task(**params)
    db.add(task)
    db.commit()

@with_db_session
def update_task(task_id: str, user: User, dto: CreateTaskDto, db: Session):
    task = validate_task(task_id, user, db)
    task.summary = dto.summary
    task.description = dto.description
    db.commit()

@with_db_session
def update_task_status(task_id: str, status: TaskStatus, user: User, db: Session):
    task = validate_task(task_id, user, db)
    task.status = status
    db.commit()

@with_db_session
def update_task_priority(task_id: str, priority: TaskPriority, user: User, db: Session):
    task = validate_task(task_id, user, db)
    task.priority = priority
    db.commit()

@with_db_session
def validate_task(task_id: str, user: User, db: Session):
    task = db.query(Task).filter(Task.id == task_id).first()
    if not task:
        raise NotFoundException()
    if task.created_by != user.id:
        raise ForbiddenException()
    return task
