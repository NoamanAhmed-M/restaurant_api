from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from fastapi import HTTPException, status
from typing import Optional

from ..models.user import User
from ..schemas import UserUpdate, UserRole

async def get_user(db: AsyncSession, user_id: str) -> Optional[User]:
    """Get a single user by ID"""
    result = await db.execute(select(User).where(User.user_id == user_id))
    return result.scalars().first()

async def get_users(db: AsyncSession, skip: int = 0, limit: int = 100):
    """Get multiple users with pagination"""
    result = await db.execute(select(User).offset(skip).limit(limit))
    return result.scalars().all()

async def create_user(db: AsyncSession, user_data: dict) -> User:
    """Create a new user"""
    db_user = User(**user_data)
    db.add(db_user)
    await db.commit()
    await db.refresh(db_user)
    return db_user

async def update_user(db: AsyncSession, user_id: str, user_data: UserUpdate) -> Optional[User]:
    """Update an existing user"""
    result = await db.execute(select(User).where(User.user_id == user_id))
    db_user = result.scalars().first()
    
    if not db_user:
        return None
    
    update_data = user_data.model_dump(exclude_unset=True)
    
    for field, value in update_data.items():
        setattr(db_user, field, value)
    
    await db.commit()
    await db.refresh(db_user)
    return db_user

async def delete_user(db: AsyncSession, user_id: str) -> bool:
    """Delete a user"""
    result = await db.execute(select(User).where(User.user_id == user_id))
    db_user = result.scalars().first()
    
    if not db_user:
        return False
    
    await db.delete(db_user)
    await db.commit()
    return True

async def change_user_role(db: AsyncSession, user_id: str, new_role: UserRole) -> Optional[User]:
    """Change a user's role"""
    result = await db.execute(select(User).where(User.user_id == user_id))
    db_user = result.scalars().first()
    
    if not db_user:
        return None
    
    db_user.role = new_role
    await db.commit()
    await db.refresh(db_user)
    return db_user