from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List

from ..schemas import UserResponse, UserUpdate, UserRole  # Added UserRole import
from ..schemas.user import UserCreate
from ..services.user_service import (
    get_user,
    get_users,
    create_user,
    update_user,
    delete_user,
    change_user_role
)
from ..database import get_db
from ..services.auth import get_current_active_user, get_current_admin_user

router = APIRouter(
    prefix="/users",
    tags=["Users"]
)

@router.post("/", response_model=UserResponse)
async def create_new_user(
    user: UserCreate,
    db: AsyncSession = Depends(get_db),
    current_user: UserResponse = Depends(get_current_admin_user)
):
    """Create a new user (admin only)"""
    return await create_user(db, user.model_dump())

@router.get("/", response_model=List[UserResponse])
async def read_users(
    skip: int = 0,
    limit: int = 100,
    db: AsyncSession = Depends(get_db),
    current_user: UserResponse = Depends(get_current_admin_user)
):
    """Get all users (admin only)"""
    return await get_users(db, skip=skip, limit=limit)

@router.get("/{user_id}", response_model=UserResponse)
async def read_user(
    user_id: str,
    db: AsyncSession = Depends(get_db),
    current_user: UserResponse = Depends(get_current_active_user)
):
    """Get a specific user"""
    db_user = await get_user(db, user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user

@router.put("/{user_id}", response_model=UserResponse)
async def update_existing_user(
    user_id: str,
    user: UserUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: UserResponse = Depends(get_current_active_user)
):
    """Update a user"""
    db_user = await update_user(db, user_id, user)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user

@router.delete("/{user_id}")
async def remove_user(
    user_id: str,
    db: AsyncSession = Depends(get_db),
    current_user: UserResponse = Depends(get_current_admin_user)
):
    """Delete a user (admin only)"""
    success = await delete_user(db, user_id)
    if not success:
        raise HTTPException(status_code=404, detail="User not found")
    return {"message": "User deleted successfully"}

@router.patch("/{user_id}/role", response_model=UserResponse)
async def update_user_role(
    user_id: str,
    role: UserRole,  # Now properly imported
    db: AsyncSession = Depends(get_db),
    current_user: UserResponse = Depends(get_current_admin_user)
):
    """Change a user's role (admin only)"""
    db_user = await change_user_role(db, user_id, role)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user