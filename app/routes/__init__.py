"""
Main application package initialization

Exports the FastAPI application and shared components
"""

from fastapi import FastAPI
from ..database import Base, engine, get_db

# Initialize database tables (in production, use migrations instead)
async def create_tables():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

# Export core components
__all__ = [
    'Base',
    'engine',
    'get_db',
    'create_tables'
]