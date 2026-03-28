from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime
from .user import RoleEnum

class UserRegister(BaseModel):
    full_name: str
    email: EmailStr
    password: str
    role: RoleEnum = RoleEnum.employee

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class UserResponse(BaseModel):
    id: int
    full_name: str
    email: str
    role: RoleEnum
    created_at: datetime

    class Config:
        from_attributes = True

class Token(BaseModel):
    access_token: str
    token_type: str
    user: UserResponse