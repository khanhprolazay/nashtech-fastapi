from fastapi import APIRouter, status, Depends, Path
from services.auth import authenticate, get_user
from schemas.user import User
from models.task import CreateTaskDto, UpdateTaskDto
from models.view import TaskViewModel
import services.task as task_service
from sqlalchemy.orm import Session
from database import get_session
from uuid import UUID
from schemas.task import TaskStatus, TaskPriority

router = APIRouter(prefix="/task", tags=["tasks"])

@router.get("", dependencies=[Depends(authenticate)], response_model=list[TaskViewModel])
async def get_tasks(user: User = Depends(get_user)):
    return user.tasks

@router.post("", dependencies=[Depends(authenticate)], status_code=status.HTTP_201_CREATED)
async def create_task(dto: CreateTaskDto, user: User = Depends(get_user), db: Session = Depends(get_session)):
    return task_service.create_task(user, dto, db)

@router.patch("/{task_id}", dependencies=[Depends(authenticate)], status_code=status.HTTP_204_NO_CONTENT)
async def update_task(
    dto: UpdateTaskDto, 
    task_id: UUID = Path(..., title="Task id is not valid"), 
    user: User = Depends(get_user), 
    db: Session = Depends(get_session)
):
    return task_service.update_task(task_id, user, dto, db)

@router.patch("/{task_id}/status/{status}", dependencies=[Depends(authenticate)], status_code=status.HTTP_204_NO_CONTENT)
async def update_task_status(
    task_id: UUID = Path(..., title="Task id is not valid"), 
    status: TaskStatus = Path(..., title="Status is not valid"),
    user: User = Depends(get_user), 
    db: Session = Depends(get_session)
):
    return task_service.update_task_status(task_id, status, user, db)

@router.patch("/{task_id}/priority/{priority}", dependencies=[Depends(authenticate)], status_code=status.HTTP_204_NO_CONTENT)
async def update_task_priority(
    task_id: UUID = Path(..., title="Task id is not valid"), 
    priority: TaskPriority = Path(..., title="Priority is not valid"), 
    user: User = Depends(get_user), 
    db: Session = Depends(get_session)
):
    return task_service.update_task_priority(task_id, priority, user, db)