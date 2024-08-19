from pydantic import BaseModel
from uuid import UUID
from datetime import datetime
from schemas.task import TaskStatus, TaskPriority
from schemas.company import CompanyMode

class CompanyViewModel(BaseModel):
  id: UUID
  name: str
  description: str
  mode: CompanyMode
  rating: float
  created_at: datetime
  updated_at: datetime

  class Config:
    orm_mode = True

class UserViewModel(BaseModel):
  id: UUID
  username: str
  email: str
  first_name: str
  last_name: str
  created_at: datetime
  updated_at: datetime

  class Config:
    orm_mode = True

class TaskViewModel(BaseModel):
  id: UUID
  summary: str
  description: str
  status: TaskStatus
  priority: TaskPriority
  created_at: datetime
  updated_at: datetime

  class Config:
    orm_mode = True