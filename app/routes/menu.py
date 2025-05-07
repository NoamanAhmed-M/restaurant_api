from pydantic import BaseModel, ConfigDict
from typing import Optional, List
from uuid import UUID
from enum import Enum
from datetime import datetime

class MenuCategory(str, Enum):
    APPETIZER = "appetizer"
    MAIN = "main"
    DESSERT = "dessert"
    BEVERAGE = "beverage"
    SIDE = "side"
    ALCOHOL = "alcohol"
    BREAKFAST = "breakfast"
    LUNCH = "lunch"
    DINNER = "dinner"

class MenuProductBase(BaseModel):
    name: str
    description: Optional[str] = None
    price: float
    category: Optional[MenuCategory] = None

class MenuProductCreate(MenuProductBase):
    preparation_time: Optional[int] = None
    is_available: bool = True
    is_made_in_house: bool = True
    product_code: Optional[str] = None
    ingredients: Optional[List[UUID]] = None

class ProductIngredientBase(BaseModel):
    product_id: UUID
    ingredient_id: UUID
    quantity_required: float

class ProductIngredientCreate(ProductIngredientBase):
    pass

class ProductIngredientResponse(ProductIngredientBase):
    ingredient_name: str
    unit_of_measure: str
    model_config = ConfigDict(from_attributes=True)

class MenuProductResponse(MenuProductBase):
    product_id: UUID
    preparation_time: Optional[int]
    is_available: bool
    is_made_in_house: bool
    product_code: Optional[str]
    created_at: datetime
    updated_at: datetime
    ingredients: Optional[List[ProductIngredientResponse]] = []
    model_config = ConfigDict(from_attributes=True)

class MenuProductUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    price: Optional[float] = None
    category: Optional[MenuCategory] = None
    preparation_time: Optional[int] = None
    is_available: Optional[bool] = None
    product_code: Optional[str] = None

class MenuSection(BaseModel):
    category: MenuCategory
    products: List[MenuProductResponse] = []

class FullMenuResponse(BaseModel):
    sections: List[MenuSection] = []
    last_updated: datetime