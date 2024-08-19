from pydantic import BaseModel, Field, EmailStr
from uuid import UUID
from datetime import datetime

class CreateUserDto(BaseModel):
  username: str = Field(min_length=3)
  email: EmailStr = Field()
  password: str = Field(min_length=3)
  first_name: str = Field(min_length=3)
  last_name: str = Field(min_length=3)

class UpdateProfileDto(BaseModel):
  first_name: str = Field(min_length=3)
  last_name: str = Field(min_length=3)

class UpdatePasswordDto(BaseModel):
  old_password: str = Field(min_length=3)
  new_password: str = Field(min_length=3)

class UpdateCompanyDto(BaseModel):
  company_id: UUID = Field()