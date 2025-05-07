from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Optional
from uuid import UUID
from datetime import datetime, timedelta

from ..schemas import Reservation, Table, Client
from ..models.reservation import (
    ReservationCreate,
    ReservationResponse,
    ReservationUpdate,
    ReservationQuery
)
from ..services.reservation_service import (
    get_reservation,
    get_reservations,
    create_reservation,
    update_reservation,
    delete_reservation,
    get_available_times
)
from ..database import get_db
from ..utils.security import get_current_active_user, require_staff_or_higher

router = APIRouter(prefix="/reservations", tags=["Reservations"])

@router.post("/", response_model=ReservationResponse, status_code=status.HTTP_201_CREATED)
async def create_new_reservation(
    reservation: ReservationCreate,
    db: AsyncSession = Depends(get_db),
    current_user: dict = Depends(get_current_active_user)
):
    """
    Create a new reservation
    
    - **client_id**: UUID of the client (required)
    - **table_id**: UUID of the table (required)
    - **reservation_time**: Start time (required)
    - **duration_minutes**: Duration in minutes (default 90)
    - **notes**: Additional notes
    """
    return await create_reservation(db=db, reservation=reservation)

@router.get("/", response_model=List[ReservationResponse])
async def read_reservations(
    date: Optional[datetime] = None,
    client_id: Optional[UUID] = None,
    table_id: Optional[UUID] = None,
    skip: int = 0,
    limit: int = 100,
    db: AsyncSession = Depends(get_db),
    current_user: dict = Depends(get_current_active_user)
):
    """
    List reservations with filters
    
    - **date**: Filter by date
    - **client_id**: Filter by client
    - **table_id**: Filter by table
    - **skip**: Pagination offset
    - **limit**: Maximum results per page
    """
    query = ReservationQuery(
        date=date,
        client_id=client_id,
        table_id=table_id,
        skip=skip,
        limit=limit
    )
    return await get_reservations(db, query=query)

@router.get("/available-times", response_model=List[datetime])
async def read_available_times(
    table_id: UUID,
    date: datetime,
    duration: int = 90,
    db: AsyncSession = Depends(get_db),
    current_user: dict = Depends(get_current_active_user)
):
    """
    Get available reservation times for a table
    
    - **table_id**: UUID of the table
    - **date**: Date to check availability
    - **duration**: Desired duration in minutes
    """
    return await get_available_times(db, table_id=table_id, date=date, duration=duration)

@router.get("/{reservation_id}", response_model=ReservationResponse)
async def read_reservation(
    reservation_id: UUID,
    db: AsyncSession = Depends(get_db),
    current_user: dict = Depends(get_current_active_user)
):
    """
    Get reservation details
    
    - **reservation_id**: UUID of the reservation
    """
    db_reservation = await get_reservation(db, reservation_id=reservation_id)
    if db_reservation is None:
        raise HTTPException(status_code=404, detail="Reservation not found")
    return db_reservation

@router.put("/{reservation_id}", response_model=ReservationResponse)
async def update_reservation_details(
    reservation_id: UUID,
    reservation: ReservationUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: dict = Depends(require_staff_or_higher)
):
    """
    Update reservation information
    
    - **reservation_id**: UUID of the reservation
    - **table_id**: New table assignment
    - **reservation_time**: New time
    - **duration_minutes**: Updated duration
    """
    db_reservation = await update_reservation(db, reservation_id=reservation_id, reservation=reservation)
    if db_reservation is None:
        raise HTTPException(status_code=404, detail="Reservation not found")
    return db_reservation

@router.delete("/{reservation_id}", status_code=status.HTTP_204_NO_CONTENT)
async def cancel_reservation(
    reservation_id: UUID,
    db: AsyncSession = Depends(get_db),
    current_user: dict = Depends(get_current_active_user)
):
    """
    Cancel a reservation
    
    - **reservation_id**: UUID of the reservation to cancel
    """
    success = await delete_reservation(db, reservation_id=reservation_id)
    if not success:
        raise HTTPException(status_code=404, detail="Reservation not found")
    return None