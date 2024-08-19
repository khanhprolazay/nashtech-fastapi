from .view import UserViewModel, UUID, BaseModel, TaskPriority, TaskStatus, datetime

class CompanyTaskViewModel(BaseModel):
  id: UUID
  summary: str
  description: str
  status: TaskStatus
  priority: TaskPriority
  created_at: datetime
  updated_at: datetime 
  user: UserViewModel

  class Config:
    orm_mode = True