"""
Database models for the Job Application AI system.

Import all models here to ensure they are registered with SQLAlchemy.
This file is also used by Alembic for auto-generating migrations.
"""
from app.models.user import User
from app.models.profile import UserProfile
from app.models.project import Project
from app.models.job import Job
from app.models.application import Application
from app.models.cv import GeneratedCV, CoverLetter
from app.models.template import CVTemplate, UserJobPreferences

# Export all models
__all__ = [
    "User",
    "UserProfile",
    "Project",
    "Job",
    "Application",
    "GeneratedCV",
    "CoverLetter",
    "CVTemplate",
    "UserJobPreferences",
]
