"""
CV Template and User Job Preferences models.
"""
from sqlalchemy import Column, String, Boolean, DateTime, ForeignKey, Text
from sqlalchemy.dialects.postgresql import UUID, JSONB, ARRAY
from sqlalchemy.orm import relationship
from datetime import datetime
import uuid

from app.core.database import Base


class CVTemplate(Base):
    """
    CV template for customizing CV layout and style.
    """
    __tablename__ = "cv_templates"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String(100), nullable=False)
    description = Column(Text)

    # Template Configuration
    layout_config = Column(JSONB)  # Colors, fonts, spacing
    sections_order = Column(ARRAY(Text))  # ["summary", "experience", "projects", "skills"]

    # Preview
    thumbnail_url = Column(String(500))

    # Access Control
    is_default = Column(Boolean, default=False)
    is_public = Column(Boolean, default=True)  # User-created vs system templates
    created_by = Column(UUID(as_uuid=True), ForeignKey("auth.users.id"))

    # Timestamp
    created_at = Column(DateTime(timezone=True), nullable=False, default=datetime.utcnow)

    def __repr__(self):
        return f"<CVTemplate(id={self.id}, name={self.name})>"


class UserJobPreferences(Base):
    """
    User preferences for specific jobs (favorites, hidden, notes).
    """
    __tablename__ = "user_job_preferences"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(
        UUID(as_uuid=True),
        ForeignKey("auth.users.id", ondelete="CASCADE"),
        nullable=False
    )
    job_id = Column(
        UUID(as_uuid=True),
        ForeignKey("jobs.id", ondelete="CASCADE"),
        nullable=False
    )

    # Preferences
    is_favorited = Column(Boolean, default=False)
    is_hidden = Column(Boolean, default=False)
    custom_notes = Column(Text)

    # Timestamps
    created_at = Column(DateTime(timezone=True), nullable=False, default=datetime.utcnow)
    updated_at = Column(DateTime(timezone=True), nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)

    def __repr__(self):
        return f"<UserJobPreferences(user_id={self.user_id}, job_id={self.job_id})>"


# Create unique constraint
from sqlalchemy import Index
Index('idx_user_job_prefs_unique', UserJobPreferences.user_id, UserJobPreferences.job_id, unique=True)
