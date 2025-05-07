from pydantic import BaseModel, ConfigDict
from typing import Optional
from uuid import UUID
from datetime import datetime

class ReservationBase(BaseModel):
    client_id: UUID
    table_id: UUID
    reservation_time: datetime

class ReservationCreate(ReservationBase):
    duration_minutes: int = 90
    notes: Optional[str] = None

class ReservationResponse(ReservationBase):
    reservation_id: UUID
    duration_minutes: int
    notes: Optional[str]
    created_at: datetime
    model_config = ConfigDict(from_attributes=True)

class ReservationUpdate(BaseModel):
    table_id: Optional[UUID] = None
    reservation_time: Optional[datetime] = None
    duration_minutes: Optional[int] = None
    notes: Optional[str] = None