from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from uuid import UUID
from datetime import datetime

from ..schemas import Payment, Order
from ..models.payment import (
    PaymentCreate,
    PaymentResponse,
    PaymentMethod,
    PaymentUpdate,
    RefundRequest
)
from ..services.payment_service import (
    create_payment,
    get_payment,
    get_order_payments,
    update_payment,
    process_refund,
    get_daily_sales_summary
)
from ..database import get_db
from ..utils.security import get_current_active_user, require_staff_or_higher

router = APIRouter(prefix="/payments", tags=["Payments"])

@router.post("/", response_model=PaymentResponse, status_code=status.HTTP_201_CREATED)
async def record_payment(
    payment: PaymentCreate,
    db: AsyncSession = Depends(get_db),
    current_user: dict = Depends(require_staff_or_higher)
):
    """
    Record a new payment
    
    - **order_id**: UUID of the order (required)
    - **amount**: Payment amount (required)
    - **payment_method**: 'cash', 'card', 'online', or 'voucher'
    - **transaction_reference**: External reference ID
    """
    return await create_payment(db=db, payment=payment, staff_id=current_user.user_id)

@router.get("/order/{order_id}", response_model=List[PaymentResponse])
async def read_order_payments(
    order_id: UUID,
    db: AsyncSession = Depends(get_db),
    current_user: dict = Depends(get_current_active_user)
):
    """
    Get all payments for an order
    
    - **order_id**: UUID of the order
    """
    return await get_order_payments(db, order_id=order_id)

@router.get("/{payment_id}", response_model=PaymentResponse)
async def read_payment(
    payment_id: UUID,
    db: AsyncSession = Depends(get_db),
    current_user: dict = Depends(require_staff_or_higher)
):
    """
    Get payment details
    
    - **payment_id**: UUID of the payment
    """
    db_payment = await get_payment(db, payment_id=payment_id)
    if db_payment is None:
        raise HTTPException(status_code=404, detail="Payment not found")
    return db_payment

@router.put("/{payment_id}", response_model=PaymentResponse)
async def update_payment_details(
    payment_id: UUID,
    payment: PaymentUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: dict = Depends(require_staff_or_higher)
):
    """
    Update payment information
    
    - **payment_id**: UUID of the payment to update
    - **transaction_reference**: Updated reference ID
    - **notes**: Additional payment notes
    """
    db_payment = await update_payment(db, payment_id=payment_id, payment=payment)
    if db_payment is None:
        raise HTTPException(status_code=404, detail="Payment not found")
    return db_payment

@router.post("/{payment_id}/refund", response_model=PaymentResponse)
async def refund_payment(
    payment_id: UUID,
    refund: RefundRequest,
    db: AsyncSession = Depends(get_db),
    current_user: dict = Depends(require_staff_or_higher)
):
    """
    Process a payment refund
    
    - **payment_id**: UUID of the payment to refund
    - **amount**: Amount to refund (partial or full)
    - **reason**: Reason for refund
    """
    db_payment = await process_refund(db, payment_id=payment_id, refund=refund, staff_id=current_user.user_id)
    if db_payment is None:
        raise HTTPException(status_code=404, detail="Payment not found")
    return db_payment

@router.get("/reports/daily", response_model=List[dict])
async def read_daily_sales_report(
    date: datetime = datetime.now().date(),
    db: AsyncSession = Depends(get_db),
    current_user: dict = Depends(require_staff_or_higher)
):
    """
    Get daily sales summary
    
    - **date**: Date for report (defaults to today)
    """
    return await get_daily_sales_summary(db, date=date)