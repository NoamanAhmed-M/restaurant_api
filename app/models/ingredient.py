from pydantic import BaseModel, ConfigDict
from typing import Optional
from uuid import UUID
from datetime import datetime

class IngredientBase(BaseModel):
    name: str
    unit_of_measure: Optional[str] = None

class IngredientCreate(IngredientBase):
    current_stock: Optional[float] = 0.0
    minimum_stock: Optional[float] = None
    cost_per_unit: Optional[float] = None

class IngredientResponse(IngredientBase):
    ingredient_id: UUID
    current_stock: float
    minimum_stock: Optional[float]
    cost_per_unit: Optional[float]
    is_active: bool
    model_config = ConfigDict(from_attributes=True)

class IngredientUpdate(BaseModel):
    name: Optional[str] = None
    unit_of_measure: Optional[str] = None
    minimum_stock: Optional[float] = None
    cost_per_unit: Optional[float] = None