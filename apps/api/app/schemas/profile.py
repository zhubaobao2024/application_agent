"""
Pydantic schemas for UserProfile model.
"""
from pydantic import BaseModel, UUID4, HttpUrl
from typing import Optional, List, Dict, Any
from datetime import datetime


class UserProfileBase(BaseModel):
    """Base user profile schema."""
    full_name: str
    phone: Optional[str] = None
    location: Optional[str] = None
    linkedin_url: Optional[HttpUrl] = None
    github_url: Optional[HttpUrl] = None
    portfolio_url: Optional[HttpUrl] = None

    # Job Preferences
    target_roles: Optional[List[str]] = None
    preferred_locations: Optional[List[str]] = None
    desired_salary_min: Optional[int] = None
    desired_salary_max: Optional[int] = None
    willing_to_relocate: bool = False

    # CV Content
    summary: Optional[str] = None
    skills: Optional[Dict[str, List[str]]] = None  # {"technical": [...], "soft": [...]}
    education: Optional[List[Dict[str, Any]]] = None
    work_experience: Optional[List[Dict[str, Any]]] = None


class UserProfileCreate(UserProfileBase):
    """Schema for creating user profile."""
    user_id: UUID4


class UserProfileUpdate(BaseModel):
    """Schema for updating user profile (all fields optional)."""
    full_name: Optional[str] = None
    phone: Optional[str] = None
    location: Optional[str] = None
    linkedin_url: Optional[HttpUrl] = None
    github_url: Optional[HttpUrl] = None
    portfolio_url: Optional[HttpUrl] = None

    target_roles: Optional[List[str]] = None
    preferred_locations: Optional[List[str]] = None
    desired_salary_min: Optional[int] = None
    desired_salary_max: Optional[int] = None
    willing_to_relocate: Optional[bool] = None

    summary: Optional[str] = None
    skills: Optional[Dict[str, List[str]]] = None
    education: Optional[List[Dict[str, Any]]] = None
    work_experience: Optional[List[Dict[str, Any]]] = None


class UserProfileResponse(UserProfileBase):
    """Schema for user profile response."""
    id: UUID4
    user_id: UUID4
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}
