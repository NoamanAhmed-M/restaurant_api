from pydantic import BaseModel, EmailStr, ConfigDict
from typing import Optional, Dict, Any
from uuid import UUID
from enum import Enum
from datetime import datetime

class ClientBase(BaseModel):
    name: str
    phone: Optional[str] = None
    email: Optional[EmailStr] = None

class ClientCreate(ClientBase):
    marketing_opt_in: bool = False
    preferences: Optional[Dict[str, Any]] = None

class ClientResponse(ClientBase):
    client_id: UUID
    marketing_opt_in: bool
    loyalty_points: int
    created_at: datetime
    updated_at: datetime
    model_config = ConfigDict(from_attributes=True)

class ClientUpdate(BaseModel):
    name: Optional[str] = None
    phone: Optional[str] = None
    email: Optional[EmailStr] = None
    preferences: Optional[Dict[str, Any]] = None

class LoyaltyActivity(str, Enum):
    EARNED = "earned"
    REDEEMED = "redeemed"
    ADJUSTED = "adjusted"

class ClientWithLoyalty(ClientResponse):
    loyalty_status: Optional[str] = None
