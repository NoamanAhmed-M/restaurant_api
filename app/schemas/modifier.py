from pydantic import BaseModel, ConfigDict
from typing import Optional
from uuid import UUID

class ModifierBase(BaseModel):
    name: str
    additional_cost: float = 0.0

class ModifierCreate(ModifierBase):
    pass

class ModifierResponse(ModifierBase):
    modifier_id: UUID
    created_at: str
    model_config = ConfigDict(from_attributes=True)

class ModifierUpdate(BaseModel):
    name: Optional[str] = None
    additional_cost: Optional[float] = None