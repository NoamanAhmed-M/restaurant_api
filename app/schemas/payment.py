from pydantic import BaseModel, ConfigDict
from typing import Optional
from uuid import UUID
from enum import Enum
from datetime import datetime

class PaymentMethod(str, Enum):
    CASH = "cash"
    CARD = "card"
    ONLINE = "online"
    VOUCHER = "voucher"

class PaymentBase(BaseModel):
    order_id: UUID
    amount: float
    payment_method: PaymentMethod

class PaymentCreate(PaymentBase):
    transaction_reference: Optional[str] = None
    notes: Optional[str] = None

class PaymentResponse(PaymentBase):
    payment_id: UUID
    staff_id: UUID
    transaction_time: datetime
    transaction_reference: Optional[str]
    notes: Optional[str]
    is_refunded: bool = False
    model_config = ConfigDict(from_attributes=True)

class RefundRequest(BaseModel):
    amount: float
    reason: str