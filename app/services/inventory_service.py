from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from uuid import UUID
from typing import List

from ..schemas import Ingredient, InventoryTransaction
from ..models.inventory import StockAdjustment

async def get_ingredient(db: AsyncSession, ingredient_id: UUID):
    result = await db.execute(select(Ingredient).where(Ingredient.ingredient_id == ingredient_id))
    return result.scalars().first()

async def get_ingredients(db: AsyncSession, skip: int = 0, limit: int = 100):
    result = await db.execute(select(Ingredient).offset(skip).limit(limit))
    return result.scalars().all()

async def create_ingredient(db: AsyncSession, ingredient: dict):
    db_ingredient = Ingredient(**ingredient)
    db.add(db_ingredient)
    await db.commit()
    await db.refresh(db_ingredient)
    return db_ingredient

async def adjust_stock(db: AsyncSession, adjustment: StockAdjustment):
    ingredient = await get_ingredient(db, adjustment.ingredient_id)
    if not ingredient:
        return None
    
    if adjustment.transaction_type == "add":
        ingredient.current_stock += adjustment.quantity
    else:
        ingredient.current_stock -= adjustment.quantity
    
    transaction = InventoryTransaction(**adjustment.dict())
    db.add(transaction)
    await db.commit()
    await db.refresh(ingredient)
    return ingredient