from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Optional
from uuid import UUID

from ..schemas.client import * 
from ..models.client import (
    ClientCreate,
    ClientResponse,
    ClientUpdate,
    ClientWithLoyalty
)
from ..services.client_service import (
    get_client,
    get_clients,
    create_client,
    update_client,
    delete_client,
    get_client_with_loyalty,
    update_loyalty_points
)
from ..database import get_db
from ..utils.security import get_current_active_user

router = APIRouter(prefix="/clients", tags=["Clients"])

@router.post("/", response_model=ClientResponse, status_code=status.HTTP_201_CREATED)
async def create_new_client(
    client: ClientCreate,
    db: AsyncSession = Depends(get_db),
    current_user: Client = Depends(get_current_active_user)
):
    """
    Create a new client record
    
    - **name**: Full name of client (required)
    - **phone**: Contact number
    - **email**: Email address
    - **marketing_opt_in**: Consent for marketing emails
    """
    return await create_client(db=db, client=client)

@router.get("/", response_model=List[ClientResponse])
async def read_clients(
    skip: int = 0,
    limit: int = 100,
    db: AsyncSession = Depends(get_db),
    current_user: Client = Depends(get_current_active_user)
):
    """
    List all clients with pagination
    
    - **skip**: Number of records to skip
    - **limit**: Maximum number of records to return
    """
    clients = await get_clients(db, skip=skip, limit=limit)
    return clients

@router.get("/{client_id}", response_model=ClientWithLoyalty)
async def read_client(
    client_id: UUID,
    db: AsyncSession = Depends(get_db),
    current_user: Client = Depends(get_current_active_user)
):
    """
    Get detailed client information including loyalty points
    
    - **client_id**: UUID of the client
    """
    db_client = await get_client_with_loyalty(db, client_id=client_id)
    if db_client is None:
        raise HTTPException(status_code=404, detail="Client not found")
    return db_client

@router.put("/{client_id}", response_model=ClientResponse)
async def update_existing_client(
    client_id: UUID,
    client: ClientUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: Client = Depends(get_current_active_user)
):
    """
    Update client information
    
    - **client_id**: UUID of the client to update
    - **name**: Updated name
    - **phone**: Updated phone
    - **email**: Updated email
    - **preferences**: JSON preferences
    """
    db_client = await update_client(db, client_id=client_id, client=client)
    if db_client is None:
        raise HTTPException(status_code=404, detail="Client not found")
    return db_client

@router.delete("/{client_id}", status_code=status.HTTP_204_NO_CONTENT)
async def remove_client(
    client_id: UUID,
    db: AsyncSession = Depends(get_db),
    current_user: Client = Depends(get_current_active_user)
):
    """
    Delete a client record
    
    - **client_id**: UUID of the client to delete
    """
    success = await delete_client(db, client_id=client_id)
    if not success:
        raise HTTPException(status_code=404, detail="Client not found")
    return None

@router.post("/{client_id}/loyalty", response_model=ClientWithLoyalty)
async def adjust_loyalty_points(
    client_id: UUID,
    points: int,
    db: AsyncSession = Depends(get_db),
    current_user: Client = Depends(get_current_active_user)
):
    """
    Add or subtract loyalty points
    
    - **client_id**: UUID of the client
    - **points**: Points to add (positive) or subtract (negative)
    """
    db_client = await update_loyalty_points(db, client_id=client_id, points=points)
    if db_client is None:
        raise HTTPException(status_code=404, detail="Client not found")
    return db_client