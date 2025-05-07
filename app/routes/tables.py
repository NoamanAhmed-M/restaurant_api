from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Optional
from uuid import UUID

from ..schemas import Table
from ..models.table import (
    TableCreate,
    TableResponse,
    TableUpdate,
    TableStatus
)
from a.pp.services.table_service import (
    get_table,
    get_tables,
    create_table,
    update_table,
    delete_table,
    update_table_status
)
from ..database import get_db
from ..utils.security import get_current_active_user, require_admin_or_manager

router = APIRouter(prefix="/tables", tags=["Tables"])

@router.post("/", response_model=TableResponse, status_code=status.HTTP_201_CREATED)
async def create_new_table(
    table: TableCreate,
    db: AsyncSession = Depends(get_db),
    current_user: dict = Depends(require_admin_or_manager)
):
    """
    Add a new table
    
    - **table_number**: Unique identifier (required)
    - **capacity**: Seating capacity (required)
    - **location_description**: Physical location notes
    """
    return await create_table(db=db, table=table)

@router.get("/", response_model=List[TableResponse])
async def read_tables(
    status: Optional[TableStatus] = None,
    skip: int = 0,
    limit: int = 100,
    db: AsyncSession = Depends(get_db),
    current_user: dict = Depends(get_current_active_user)
):
    """
    List all tables with filters
    
    - **status**: Filter by status (available, occupied, reserved)
    - **skip**: Pagination offset
    - **limit**: Maximum results per page
    """
    return await get_tables(db, status=status, skip=skip, limit=limit)

@router.get("/{table_id}", response_model=TableResponse)
async def read_table(
    table_id: UUID,
    db: AsyncSession = Depends(get_db),
    current_user: dict = Depends(get_current_active_user)
):
    """
    Get table details
    
    - **table_id**: UUID of the table
    """
    db_table = await get_table(db, table_id=table_id)
    if db_table is None:
        raise HTTPException(status_code=404, detail="Table not found")
    return db_table

@router.put("/{table_id}", response_model=TableResponse)
async def update_table_details(
    table_id: UUID,
    table: TableUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: dict = Depends(require_admin_or_manager)
):
    """
    Update table information
    
    - **table_id**: UUID of the table
    - **capacity**: Updated seating capacity
    - **location_description**: Updated location notes
    """
    db_table = await update_table(db, table_id=table_id, table=table)
    if db_table is None:
        raise HTTPException(status_code=404, detail="Table not found")
    return db_table

@router.put("/{table_id}/status", response_model=TableResponse)
async def change_table_status(
    table_id: UUID,
    new_status: TableStatus,
    db: AsyncSession = Depends(get_db),
    current_user: dict = Depends(require_staff_or_higher)
):
    """
    Update table status
    
    - **table_id**: UUID of the table
    - **new_status**: 'available', 'occupied', or 'reserved'
    """
    db_table = await update_table_status(db, table_id=table_id, new_status=new_status)
    if db_table is None:
        raise HTTPException(status_code=404, detail="Table not found")
    return db_table

@router.delete("/{table_id}", status_code=status.HTTP_204_NO_CONTENT)
async def remove_table(
    table_id: UUID,
    db: AsyncSession = Depends(get_db),
    current_user: dict = Depends(require_admin_or_manager)
):
    """
    Remove a table (hard delete)
    
    - **table_id**: UUID of the table to remove
    """
    success = await delete_table(db, table_id=table_id)
    if not success:
        raise HTTPException(status_code=404, detail="Table not found")
    return None