from sqlalchemy import Column, Uuid, DateTime
from uuid import uuid4, UUID
from datetime import datetime
from enum import Enum

class BaseEntity():
  id = Column(Uuid, primary_key=True, default=uuid4)
  created_at = Column(DateTime, default=datetime.now)
  updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)

  def to_dict(self):
    result = {}
    for column in self.__table__.columns:
      value = getattr(self, column.name)

      if isinstance(value, (datetime, UUID)):
        value = str(value)

      if isinstance(value, Enum):
        value = value.value

      result[column.name] = value
    return result