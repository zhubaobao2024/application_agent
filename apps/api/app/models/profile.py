"""
User Profile model with personal information and preferences.
"""
from sqlalchemy import Column, String, Integer, Boolean, DateTime, ForeignKey, Text
from sqlalchemy.dialects.postgresql import UUID, JSONB, ARRAY
from sqlalchemy.orm import relationship
from datetime import datetime
import uuid

from app.core.database import Base


class UserProfile(Base):
    """
    User profile with personal information, preferences, and base CV content.
    """
    __tablename__ = "user_profiles"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(
        UUID(as_uuid=True),
        ForeignKey("auth.users.id", ondelete="CASCADE"),
        unique=True,
        nullable=False,
        index=True
    )

    # Personal Information
    full_name = Column(String(255), nullable=False)
    phone = Column(String(50))
    location = Column(String(255))
    linkedin_url = Column(String(500))
    github_url = Column(String(500))
    portfolio_url = Column(String(500))

    # Job Preferences
    target_roles = Column(ARRAY(Text))  # ["Software Engineer", "ML Engineer"]
    preferred_locations = Column(ARRAY(Text))  # ["Remote", "San Francisco"]
    desired_salary_min = Column(Integer)
    desired_salary_max = Column(Integer)
    willing_to_relocate = Column(Boolean, default=False)

    # Base CV Content
    summary = Column(Text)  # Professional summary
    skills = Column(JSONB)  # {"technical": ["Python", "React"], "soft": [...]}
    education = Column(JSONB)  # Array of education entries
    work_experience = Column(JSONB)  # Array of work experience entries

    # Timestamps
    created_at = Column(DateTime(timezone=True), nullable=False, default=datetime.utcnow)
    updated_at = Column(DateTime(timezone=True), nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    user = relationship("User", back_populates="profile")

    def __repr__(self):
        return f"<UserProfile(id={self.id}, full_name={self.full_name})>"
