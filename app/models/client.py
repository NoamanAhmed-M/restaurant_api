from sqlalchemy import Column, String, Integer, Boolean, JSON, DateTime
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from sqlalchemy.sql import func
from app.database import Base
import uuid

class Client(Base):
    __tablename__ = "clients"

    client_id = Column(PG_UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String(100), nullable=False)
    phone = Column(String(20))
    email = Column(String(255))
    loyalty_points = Column(Integer, default=0)
    preferences = Column(JSON)
    marketing_opt_in = Column(Boolean, default=False)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())
