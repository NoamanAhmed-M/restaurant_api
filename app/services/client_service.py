from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from fastapi import HTTPException, status
from typing import Optional

from ..models.client import Client
from ..schemas import ClientCreate, ClientUpdate

async def get_client(db: AsyncSession, client_id: str) -> Optional[Client]:
    """Get a single client by ID"""
    result = await db.execute(select(Client).where(Client.client_id == client_id))
    return result.scalars().first()

async def get_clients(db: AsyncSession, skip: int = 0, limit: int = 100):
    """Get multiple clients with pagination"""
    result = await db.execute(select(Client).offset(skip).limit(limit))
    return result.scalars().all()

async def create_client(db: AsyncSession, client: ClientCreate) -> Client:
    """Create a new client"""
    db_client = Client(**client.model_dump())
    db.add(db_client)
    await db.commit()
    await db.refresh(db_client)
    return db_client

async def update_client(db: AsyncSession, client_id: str, client: ClientUpdate) -> Optional[Client]:
    """Update client information"""
    result = await db.execute(select(Client).where(Client.client_id == client_id))
    db_client = result.scalars().first()
    
    if not db_client:
        return None
    
    update_data = client.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_client, field, value)
    
    await db.commit()
    await db.refresh(db_client)
    return db_client

async def update_loyalty_points(db: AsyncSession, client_id: str, points: int) -> Optional[Client]:
    """Update client's loyalty points"""
    result = await db.execute(select(Client).where(Client.client_id == client_id))
    db_client = result.scalars().first()
    
    if not db_client:
        return None
    
    db_client.loyalty_points = points
    await db.commit()
    await db.refresh(db_client)
    return db_client

async def delete_client(db: AsyncSession, client_id: str) -> bool:
    """Delete a client"""
    result = await db.execute(select(Client).where(Client.client_id == client_id))
    db_client = result.scalars().first()
    
    if not db_client:
        return False
    
    await db.delete(db_client)
    await db.commit()
    return True