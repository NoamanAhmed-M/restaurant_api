from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from uuid import UUID
from typing import List

from ..schemas import Order, OrderItem
from ..models.order import OrderCreate

async def get_order(db: AsyncSession, order_id: UUID):
    result = await db.execute(select(Order).where(Order.order_id == order_id))
    return result.scalars().first()

async def get_orders(db: AsyncSession, skip: int = 0, limit: int = 100):
    result = await db.execute(select(Order).offset(skip).limit(limit))
    return result.scalars().all()

async def create_order(db: AsyncSession, order: OrderCreate):
    db_order = Order(**order.dict())
    db.add(db_order)
    await db.commit()
    await db.refresh(db_order)
    return db_order

async def add_order_item(db: AsyncSession, order_id: UUID, item: dict):
    db_item = OrderItem(order_id=order_id, **item)
    db.add(db_item)
    await db.commit()
    await db.refresh(db_item)
    return db_item

async def update_order_status(db: AsyncSession, order_id: UUID, status: str):
    order = await get_order(db, order_id)
    if not order:
        return None
    
    order.status = status
    await db.commit()
    await db.refresh(order)
    return order