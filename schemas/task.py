from .base_entity import BaseEntity
from sqlalchemy import Column, String, Enum, ForeignKey
from sqlalchemy.orm import relationship
from database import Base
import enum
from .user import User

class TaskPriority(enum.Enum):
    LOW = 'low'
    MEDIUM = 'medium'
    HIGH = 'high'

class TaskStatus(enum.Enum):
    OPEN = 'open'
    IN_PROGRESS = 'in_progress'
    DONE = 'done'

class Task(Base, BaseEntity):
    __tablename__ = "tasks"

    summary = Column(String, nullable=False)
    description = Column(String, nullable=True)
    priority = Column(Enum(TaskPriority), default=TaskPriority.LOW, nullable=False)
    status = Column(Enum(TaskStatus), default=TaskStatus.OPEN, nullable=False)

    created_by = Column(String, ForeignKey("users.id"))
    user = relationship("User", back_populates="tasks", foreign_keys=[created_by])

User.tasks = relationship("Task", back_populates="user")