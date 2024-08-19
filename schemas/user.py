from .base_entity import BaseEntity
from sqlalchemy import Column, String, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from database import Base
from datetime import datetime
from .company import Company

class User(Base, BaseEntity):
    __tablename__ = "users"
    
    email = Column(String, nullable=False, unique=True)
    username = Column(String, nullable=False, unique=True)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    hashed_password = Column(String, nullable=False)
    is_active = Column(Boolean, default=True)
    is_admin = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)

    company_id = Column(String, ForeignKey("companies.id"))
    company = relationship("Company", back_populates="users")

    def to_dict(self):
        result = super().to_dict()
        result.pop("hashed_password")
        if self.company:
            result.update({"company": self.company.to_dict()})
        return result

Company.users = relationship("User", back_populates="company")

