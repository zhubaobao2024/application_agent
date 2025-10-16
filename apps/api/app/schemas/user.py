"""
Pydantic schemas for User model.
"""
from pydantic import BaseModel, EmailStr, UUID4
from typing import Optional
from datetime import datetime


class UserBase(BaseModel):
    """Base user schema."""
    email: EmailStr


class UserCreate(UserBase):
    """Schema for user creation (signup)."""
    password: str
    full_name: str


class UserLogin(BaseModel):
    """Schema for user login."""
    email: EmailStr
    password: str


class UserResponse(UserBase):
    """Schema for user response."""
    id: UUID4
    created_at: datetime
    email_confirmed_at: Optional[datetime] = None

    model_config = {"from_attributes": True}


class Token(BaseModel):
    """JWT token response."""
    access_token: str
    token_type: str = "bearer"
    expires_at: datetime


class TokenData(BaseModel):
    """Data stored in JWT token."""
    user_id: Optional[UUID4] = None
    email: Optional[str] = None
