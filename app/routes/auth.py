from datetime import datetime, timedelta
from typing import Optional
from jose import JWTError, jwt
from passlib.context import CryptContext
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from ..models.user import User  # SQLAlchemy model
from ..schemas import TokenData, UserRole, UserCreate  # Pydantic schemas
from ..database import get_db

# Security setup
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/token")

# Security constants
SECRET_KEY = "your-secret-key-here"  # Replace with a strong secret key
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# User Management Functions
async def create_user(db: AsyncSession, user_create: UserCreate, hashed_password: str) -> User:
    """Create a new user in the database"""
    db_user = User(
        username=user_create.username,
        email=user_create.email,
        hashed_password=hashed_password,
        role=user_create.role,
        is_active=True
    )
    db.add(db_user)
    await db.commit()
    await db.refresh(db_user)
    return db_user

async def get_user_by_username(db: AsyncSession, username: str) -> Optional[User]:
    """Get a user by username"""
    result = await db.execute(select(User).where(User.username == username))
    return result.scalars().first()

# Authentication Functions
async def authenticate_user(db: AsyncSession, username: str, password: str) -> Optional[User]:
    """Authenticate a user with username and password"""
    user = await get_user_by_username(db, username)
    if not user or not verify_password(password, user.hashed_password):
        return None
    return user

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify a plain password against the hashed version"""
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password: str) -> str:
    """Generate a password hash"""
    return pwd_context.hash(password)

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    """Create a JWT access token with expiration"""
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

# Current User Dependencies
async def get_current_user(
    db: AsyncSession = Depends(get_db),
    token: str = Depends(oauth2_scheme)
) -> User:
    """Get the current authenticated user from JWT token"""
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        user_id: str = payload.get("user_id")
        role: str = payload.get("role")
        
        if not username or not user_id:
            raise credentials_exception
            
        token_data = TokenData(
            username=username,
            user_id=user_id,
            role=UserRole(role) if role else None
        )
    except (JWTError, ValueError):
        raise credentials_exception
    
    user = await db.execute(select(User).where(User.user_id == token_data.user_id))
    user = user.scalars().first()
    if user is None:
        raise credentials_exception
    return user

async def get_current_active_user(
    current_user: User = Depends(get_current_user)
) -> User:
    """Verify the current user is active"""
    if not current_user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Inactive user"
        )
    return current_user

async def get_current_admin_user(
    current_user: User = Depends(get_current_user)
) -> User:
    """Verify the current user is an admin"""
    if current_user.role != UserRole.ADMIN:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin privileges required"
        )
    return current_user