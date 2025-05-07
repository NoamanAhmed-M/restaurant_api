from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from uuid import UUID
from typing import List

from ..schemas import Table

async def get_table(db: AsyncSession, table_id: UUID):
    result = await db.execute(select(Table).where(Table.table_id == table_id))
    return result.scalars().first()

async def get_tables(db: AsyncSession, skip: int = 0, limit: int = 100):
    result = await db.execute(select(Table).offset(skip).limit(limit))
    return result.scalars().all()

async def create_table(db: AsyncSession, table: dict):
    db_table = Table(**table)
    db.add(db_table)
    await db.commit()
    await db.refresh(db_table)
    return db_table

async def update_table_status(db: AsyncSession, table_id: UUID, status: str):
    table = await get_table(db, table_id)
    if not table:
        return None
    
    table.status = status
    await db.commit()
    await db.refresh(table)
    return table