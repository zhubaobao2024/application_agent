"""
Pydantic schemas for Project model.
"""
from pydantic import BaseModel, UUID4, HttpUrl
from typing import Optional, List, Dict, Any
from datetime import date, datetime


class ProjectBase(BaseModel):
    """Base project schema."""
    title: str
    description: Optional[str] = None
    detailed_description: Optional[str] = None
    technologies: Optional[List[str]] = None

    role: Optional[str] = None
    start_date: Optional[date] = None
    end_date: Optional[date] = None

    github_url: Optional[HttpUrl] = None
    demo_url: Optional[HttpUrl] = None

    achievements: Optional[List[str]] = None
    metrics: Optional[Dict[str, Any]] = None

    is_featured: bool = False
    relevance_tags: Optional[List[str]] = None


class ProjectCreate(ProjectBase):
    """Schema for creating a project."""
    pass


class ProjectUpdate(BaseModel):
    """Schema for updating a project (all fields optional)."""
    title: Optional[str] = None
    description: Optional[str] = None
    detailed_description: Optional[str] = None
    technologies: Optional[List[str]] = None

    role: Optional[str] = None
    start_date: Optional[date] = None
    end_date: Optional[date] = None

    github_url: Optional[HttpUrl] = None
    demo_url: Optional[HttpUrl] = None

    achievements: Optional[List[str]] = None
    metrics: Optional[Dict[str, Any]] = None

    is_featured: Optional[bool] = None
    relevance_tags: Optional[List[str]] = None


class ProjectResponse(ProjectBase):
    """Schema for project response."""
    id: UUID4
    user_id: UUID4
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}
