from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from uuid import UUID
from typing import List

from ..schemas import MenuProduct, ProductIngredient
from ..models.menu import MenuProductCreate

async def get_product(db: AsyncSession, product_id: UUID):
    result = await db.execute(select(MenuProduct).where(MenuProduct.product_id == product_id))
    return result.scalars().first()

async def get_products(db: AsyncSession, skip: int = 0, limit: int = 100):
    result = await db.execute(select(MenuProduct).offset(skip).limit(limit))
    return result.scalars().all()

async def create_product(db: AsyncSession, product: MenuProductCreate):
    db_product = MenuProduct(**product.dict(exclude={"ingredients"}))
    db.add(db_product)
    await db.commit()
    await db.refresh(db_product)
    
    if product.ingredients:
        for ingredient_id in product.ingredients:
            await add_product_ingredient(db, db_product.product_id, ingredient_id, 0)  # Default quantity
    
    return db_product

async def add_product_ingredient(db: AsyncSession, product_id: UUID, ingredient_id: UUID, quantity: float):
    db_ingredient = ProductIngredient(
        product_id=product_id,
        ingredient_id=ingredient_id,
        quantity_required=quantity
    )
    db.add(db_ingredient)
    await db.commit()
    await db.refresh(db_ingredient)
    return db_ingredient