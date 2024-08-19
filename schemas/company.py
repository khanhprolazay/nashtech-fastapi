from .base_entity import BaseEntity
from sqlalchemy import Column, String, Numeric, Enum
from database import Base
import enum
from typing import List

class CompanyMode(enum.Enum):
  PRIVATE = 'private'
  PUBLIC = 'public'

class Company(Base, BaseEntity):
  __tablename__ = "companies"

  name = Column(String, nullable=False)
  description = Column(String, nullable=True)
  mode = Column(Enum(CompanyMode), default=CompanyMode.PRIVATE, nullable=False)
  rating = Column(Numeric, nullable=True)