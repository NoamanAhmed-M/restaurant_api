from datetime import datetime, timedelta
from typing import Any, Dict, Optional
from uuid import UUID
import json

def serialize_json(data: Any) -> str:
    """Serialize data to JSON with UUID and datetime support"""
    def default_serializer(o):
        if isinstance(o, UUID):
            return str(o)
        if isinstance(o, datetime):
            return o.isoformat()
        if isinstance(o, timedelta):
            return str(o)
        raise TypeError(f"Object of type {o.__class__.__name__} is not JSON serializable")
    return json.dumps(data, default=default_serializer)

def generate_order_number() -> str:
    """Generate a human-readable order number"""
    now = datetime.now()
    return f"ORD-{now.year}{now.month:02d}{now.day:02d}-{now.hour:02d}{now.minute:02d}"

def calculate_estimated_wait_time(order_items: list) -> int:
    """Calculate estimated preparation time in minutes"""
    return sum(item.get('preparation_time', 0) for item in order_items) or 15

def validate_time_slot(start_time: datetime, duration: int) -> bool:
    """Validate if a time slot is reasonable"""
    if duration <= 0 or duration > 240:  # 4 hours max
        return False
    if start_time < datetime.now():
        return False
    return True

async def send_notification(user_id: UUID, message: str):
    """Placeholder for notification system"""
    # Would integrate with email/SMS/websocket in production
    print(f"Notification to {user_id}: {message}")