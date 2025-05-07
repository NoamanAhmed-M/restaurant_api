from uuid import uuid4
from datetime import datetime
from enum import Enum as PyEnum
from sqlalchemy import Column, String, Boolean, DateTime
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from sqlalchemy.sql import func
from sqlalchemy import Enum as SAEnum
from app.database import Base

class UserRole(str, PyEnum):
    ADMIN = "admin"
    MANAGER = "manager"
    STAFF = "staff"

class User(Base):
    __tablename__ = "users"

    user_id = Column(PG_UUID(as_uuid=True), primary_key=True, default=uuid4)
    username = Column(String(50), unique=True, index=True, nullable=False)
    email = Column(String(255), unique=True, index=True)
    hashed_password = Column(String(255), nullable=False)
    role = Column(SAEnum(UserRole, name="user_roles"), nullable=False)
    is_active = Column(Boolean, default=True)
    last_login = Column(DateTime(timezone=True))
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())