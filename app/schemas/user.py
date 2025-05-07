from uuid import UUID
from datetime import datetime
from enum import Enum
from typing import Optional
from pydantic import BaseModel, EmailStr, ConfigDict

class UserRole(str, Enum):
    ADMIN = "admin"
    MANAGER = "manager"
    STAFF = "staff"

class UserBase(BaseModel):
    username: str
    email: Optional[EmailStr] = None
    role: UserRole

class UserCreate(UserBase):
    password: str

class UserResponse(UserBase):
    user_id: UUID
    is_active: bool
    last_login: Optional[datetime] = None
    created_at: datetime
    updated_at: datetime
    model_config = ConfigDict(from_attributes=True)

class UserUpdate(BaseModel):
    email: Optional[EmailStr] = None
    role: Optional[UserRole] = None

class UserLogin(BaseModel):
    username: str
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str
    user: UserResponse

class TokenData(BaseModel):
    username: Optional[str] = None
    user_id: Optional[UUID] = None
    scopes: list[str] = []
    role: Optional[UserRole] = None
