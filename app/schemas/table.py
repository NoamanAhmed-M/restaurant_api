from pydantic import BaseModel, ConfigDict
from typing import Optional
from uuid import UUID
from enum import Enum

class TableStatus(str, Enum):
    AVAILABLE = "available"
    OCCUPIED = "occupied"
    RESERVED = "reserved"
    MAINTENANCE = "maintenance"

class TableBase(BaseModel):
    table_number: str
    capacity: int

class TableCreate(TableBase):
    location_description: Optional[str] = None

class TableResponse(TableBase):
    table_id: UUID
    location_description: Optional[str]
    status: TableStatus
    is_reserved: bool
    model_config = ConfigDict(from_attributes=True)

class TableUpdate(BaseModel):
    capacity: Optional[int] = None
    location_description: Optional[str] = None