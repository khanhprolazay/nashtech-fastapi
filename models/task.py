from pydantic import BaseModel, Field
from uuid import UUID
from datetime import datetime
from schemas.task import TaskPriority, TaskStatus

class CreateTaskDto(BaseModel):
  summary: str = Field(min_length=3)
  description: str = Field()
  status: TaskStatus = Field(default=TaskStatus.OPEN)
  priority: TaskPriority = Field(default=TaskPriority.LOW)

class UpdateTaskDto(BaseModel):
  summary: str = Field(min_length=3)
  description: str = Field()