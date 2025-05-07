import os
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy.pool import NullPool
from dotenv import load_dotenv
from typing import AsyncGenerator
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()

# Database configuration
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql+asyncpg://user:password@localhost:5432/restaurant_db")
TEST_DATABASE_URL = os.getenv("TEST_DATABASE_URL", "postgresql+asyncpg://user:password@localhost:5432/restaurant_test")

# Determine which database URL to use
if os.getenv("TESTING", "").lower() == "true":
    DATABASE_URL = TEST_DATABASE_URL
    logger.info("Using TEST database")
else:
    logger.info("Using PRODUCTION database")

# Create async engine
engine = create_async_engine(
    DATABASE_URL,
    echo=True if os.getenv("SQL_ECHO", "False").lower() == "true" else False,
    poolclass=NullPool if os.getenv("TESTING") else None,
    future=True
)

# Session factory
AsyncSessionLocal = sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autoflush=False
)

# Base class for models
Base = declarative_base()

async def get_db() -> AsyncGenerator[AsyncSession, None]:
    """
    Dependency that provides a database session.
    Properly handles session cleanup after request completion.
    """
    async with AsyncSessionLocal() as session:
        try:
            yield session
            await session.commit()
        except Exception as e:
            logger.error(f"Database error: {e}")
            await session.rollback()
            raise
        finally:
            await session.close()

async def init_db():
    """Initialize database tables (for development/testing)"""
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    logger.info("Database tables initialized")

async def drop_db():
    """Drop all tables (for testing)"""
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
    logger.info("Database tables dropped")

# Export important components
__all__ = [
    "Base",
    "engine",
    "get_db",
    "init_db",
    "drop_db",
    "AsyncSessionLocal"
]