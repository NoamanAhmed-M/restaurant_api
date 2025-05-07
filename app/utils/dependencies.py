from fastapi import Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Annotated
from uuid import UUID

from ..database import get_db
from ..schemas import UserResponse  
from ..utils.security import get_current_active_user

async def get_current_staff_user(
    current_user: Annotated[UserResponse, Depends(get_current_active_user)]
):
    """Dependency to verify staff or higher role"""
    if current_user.role not in ["staff", "manager", "admin"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Operation requires staff privileges"
        )
    return current_user

async def get_current_manager_user(
    current_user: Annotated[UserResponse, Depends(get_current_active_user)]
):
    """Dependency to verify manager or admin role"""
    if current_user.role not in ["manager", "admin"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Operation requires manager privileges"
        )
    return current_user

async def get_current_admin_user(
    current_user: Annotated[UserResponse, Depends(get_current_active_user)]
):
    """Dependency to verify admin role"""
    if current_user.role != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Operation requires admin privileges"
        )
    return current_user

async def validate_table_id(
    table_id: UUID,
    db: AsyncSession = Depends(get_db)
):
    """Dependency to validate table exists"""
    from ..services.table_service import get_table
    table = await get_table(db, table_id)
    if not table:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Table not found"
        )
    return table_id