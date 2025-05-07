from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from uuid import UUID
from datetime import datetime
from typing import List

from ..schemas import Reservation

async def get_reservation(db: AsyncSession, reservation_id: UUID):
    result = await db.execute(select(Reservation).where(Reservation.reservation_id == reservation_id))
    return result.scalars().first()

async def get_reservations(db: AsyncSession, skip: int = 0, limit: int = 100):
    result = await db.execute(select(Reservation).offset(skip).limit(limit))
    return result.scalars().all()

async def create_reservation(db: AsyncSession, reservation: dict):
    db_reservation = Reservation(**reservation)
    db.add(db_reservation)
    await db.commit()
    await db.refresh(db_reservation)
    return db_reservation

async def check_table_availability(db: AsyncSession, table_id: UUID, start_time: datetime, duration: int):
    # Implementation would check for overlapping reservations
    return True