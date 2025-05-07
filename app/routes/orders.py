from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Optional
from uuid import UUID
from datetime import datetime

from ..schemas import Order, OrderItem, OrderItemModifier
from ..models.order import (
    OrderCreate,
    OrderResponse,
    OrderUpdate,
    OrderStatus,
    OrderItemCreate,
    OrderItemModifierCreate
)
from ..services.order_service import (
    get_order,
    get_orders,
    create_order,
    update_order,
    delete_order,
    add_order_item,
    update_order_status,
    add_modifier_to_item,
    get_kitchen_orders,
    get_table_orders
)
from ..database import get_db
from ..utils.security import get_current_active_user, require_staff_or_higher

router = APIRouter(prefix="/orders", tags=["Orders"])

@router.post("/", response_model=OrderResponse, status_code=status.HTTP_201_CREATED)
async def create_new_order(
    order: OrderCreate,
    db: AsyncSession = Depends(get_db),
    current_user: dict = Depends(require_staff_or_higher)
):
    """
    Create a new order
    
    - **table_id**: UUID of the table (required)
    - **server_id**: UUID of the staff member
    - **client_id**: UUID of the client (optional)
    - **items**: List of order items
    """
    return await create_order(db=db, order=order, server_id=current_user.user_id)

@router.get("/", response_model=List[OrderResponse])
async def read_orders(
    skip: int = 0,
    limit: int = 100,
    status: Optional[OrderStatus] = None,
    db: AsyncSession = Depends(get_db),
    current_user: dict = Depends(get_current_active_user)
):
    """
    List all orders with filters
    
    - **skip**: Pagination offset
    - **limit**: Maximum results per page
    - **status**: Filter by order status
    """
    return await get_orders(db, skip=skip, limit=limit, status=status)

@router.get("/kitchen", response_model=List[OrderResponse])
async def read_kitchen_orders(
    db: AsyncSession = Depends(get_db),
    current_user: dict = Depends(require_staff_or_higher)
):
    """
    Get orders that need kitchen preparation
    (status: pending or preparing)
    """
    return await get_kitchen_orders(db)

@router.get("/table/{table_id}", response_model=List[OrderResponse])
async def read_table_orders(
    table_id: UUID,
    active_only: bool = True,
    db: AsyncSession = Depends(get_db),
    current_user: dict = Depends(get_current_active_user)
):
    """
    Get orders for a specific table
    
    - **table_id**: UUID of the table
    - **active_only**: Only show non-completed orders (default True)
    """
    return await get_table_orders(db, table_id=table_id, active_only=active_only)

@router.get("/{order_id}", response_model=OrderResponse)
async def read_order(
    order_id: UUID,
    db: AsyncSession = Depends(get_db),
    current_user: dict = Depends(get_current_active_user)
):
    """
    Get detailed order information
    
    - **order_id**: UUID of the order
    """
    db_order = await get_order(db, order_id=order_id)
    if db_order is None:
        raise HTTPException(status_code=404, detail="Order not found")
    return db_order

@router.put("/{order_id}", response_model=OrderResponse)
async def update_order_details(
    order_id: UUID,
    order: OrderUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: dict = Depends(require_staff_or_higher)
):
    """
    Update order information
    
    - **order_id**: UUID of the order to update
    - **client_id**: Updated client reference
    - **notes**: General order notes
    """
    db_order = await update_order(db, order_id=order_id, order=order)
    if db_order is None:
        raise HTTPException(status_code=404, detail="Order not found")
    return db_order

@router.put("/{order_id}/status", response_model=OrderResponse)
async def change_order_status(
    order_id: UUID,
    new_status: OrderStatus,
    db: AsyncSession = Depends(get_db),
    current_user: dict = Depends(require_staff_or_higher)
):
    """
    Update order status
    
    - **order_id**: UUID of the order
    - **new_status**: New status (pending, preparing, ready, delivered, cancelled)
    """
    db_order = await update_order_status(db, order_id=order_id, new_status=new_status)
    if db_order is None:
        raise HTTPException(status_code=404, detail="Order not found")
    return db_order

@router.post("/{order_id}/items", response_model=OrderItem)
async def add_item_to_order(
    order_id: UUID,
    item: OrderItemCreate,
    db: AsyncSession = Depends(get_db),
    current_user: dict = Depends(require_staff_or_higher)
):
    """
    Add an item to an existing order
    
    - **order_id**: UUID of the order
    - **product_id**: UUID of the menu product
    - **quantity**: Item quantity
    - **notes**: Special instructions
    """
    return await add_order_item(db, order_id=order_id, item=item)

@router.post("/items/{item_id}/modifiers", response_model=OrderItemModifier)
async def add_modifier_to_order_item(
    item_id: UUID,
    modifier: OrderItemModifierCreate,
    db: AsyncSession = Depends(get_db),
    current_user: dict = Depends(require_staff_or_higher)
):
    """
    Add a modifier to an order item
    
    - **item_id**: UUID of the order item
    - **modifier_id**: UUID of the product modifier
    """
    return await add_modifier_to_item(db, item_id=item_id, modifier_id=modifier.modifier_id)

@router.delete("/{order_id}", status_code=status.HTTP_204_NO_CONTENT)
async def cancel_order(
    order_id: UUID,
    db: AsyncSession = Depends(get_db),
    current_user: dict = Depends(require_staff_or_higher)
):
    """
    Cancel an order (soft delete)
    
    - **order_id**: UUID of the order to cancel
    """
    success = await delete_order(db, order_id=order_id)
    if not success:
        raise HTTPException(status_code=404, detail="Order not found")
    return None