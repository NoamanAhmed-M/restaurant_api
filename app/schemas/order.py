from pydantic import BaseModel, ConfigDict
from typing import Optional, List
from uuid import UUID
from enum import Enum
from datetime import datetime
from .order_item import OrderItemResponse, OrderItemCreate

class OrderStatus(str, Enum):
    PENDING = "pending"
    PREPARING = "preparing"
    READY = "ready"
    DELIVERED = "delivered"
    CANCELLED = "cancelled"

class OrderBase(BaseModel):
    table_id: UUID
    client_id: Optional[UUID] = None
    notes: Optional[str] = None

class OrderCreate(OrderBase):
    items: Optional[List[OrderItemCreate]] = []

class OrderResponse(OrderBase):
    order_id: UUID
    server_id: UUID
    order_time: datetime
    status: OrderStatus
    total_amount: float
    payment_status: str
    items: List[OrderItemResponse] = []
    created_at: datetime
    updated_at: datetime
    model_config = ConfigDict(from_attributes=True)

class OrderUpdate(BaseModel):
    client_id: Optional[UUID] = None
    notes: Optional[str] = None