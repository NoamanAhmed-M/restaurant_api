from pydantic import BaseModel, ConfigDict
from typing import Optional
from uuid import UUID
from enum import Enum
from datetime import datetime

class TransactionType(str, Enum):
    ADD = "add"
    USE = "use"
    SPOIL = "spoil"
    ADJUST = "adjust"

class InventoryTransactionBase(BaseModel):
    ingredient_id: UUID
    quantity: float
    transaction_type: TransactionType

class InventoryTransactionCreate(InventoryTransactionBase):
    reference: Optional[str] = None

class InventoryTransactionResponse(InventoryTransactionBase):
    transaction_id: UUID
    transaction_time: datetime
    reference: Optional[str]
    staff_id: UUID
    model_config = ConfigDict(from_attributes=True)

class StockAdjustment(BaseModel):
    quantity: float
    transaction_type: TransactionType
    notes: Optional[str] = None