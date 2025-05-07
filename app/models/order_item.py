from pydantic import BaseModel, ConfigDict
from typing import Optional, List
from uuid import UUID
from .modifier import ModifierResponse

class OrderItemBase(BaseModel):
    product_id: UUID
    quantity: int = 1

class OrderItemCreate(OrderItemBase):
    notes: Optional[str] = None
    modifiers: Optional[List[UUID]] = []

class OrderItemResponse(OrderItemBase):
    item_id: UUID
    unit_price: float
    notes: Optional[str]
    modifiers: List[ModifierResponse] = []
    model_config = ConfigDict(from_attributes=True)