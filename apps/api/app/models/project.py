"""
Project model for user portfolio projects.
"""
from sqlalchemy import Column, String, Date, Boolean, DateTime, ForeignKey, Text
from sqlalchemy.dialects.postgresql import UUID, JSONB, ARRAY
from sqlalchemy.orm import relationship
from datetime import datetime
import uuid

from app.core.database import Base


class Project(Base):
    """
    User project/portfolio entry.
    Used for CV generation and matching with job requirements.
    """
    __tablename__ = "projects"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(
        UUID(as_uuid=True),
        ForeignKey("auth.users.id", ondelete="CASCADE"),
        nullable=False,
        index=True
    )

    # Project Information
    title = Column(String(255), nullable=False)
    description = Column(Text)  # Short description
    detailed_description = Column(Text)  # Detailed description for AI context
    technologies = Column(ARRAY(Text))  # ["React", "Node.js", "PostgreSQL"]

    # Timeline
    role = Column(String(100))  # "Lead Developer", "Solo Developer"
    start_date = Column(Date)
    end_date = Column(Date, nullable=True)  # NULL if ongoing

    # Links
    github_url = Column(String(500))
    demo_url = Column(String(500))

    # Achievements & Metrics
    achievements = Column(ARRAY(Text))  # Bullet points of key achievements
    metrics = Column(JSONB)  # {"users": 10000, "performance_improvement": "40%"}

    # CV Selection
    is_featured = Column(Boolean, default=False)  # Always show on CV
    relevance_tags = Column(ARRAY(Text), index=True)  # ["web", "backend", "ml"] for matching

    # Timestamps
    created_at = Column(DateTime(timezone=True), nullable=False, default=datetime.utcnow)
    updated_at = Column(DateTime(timezone=True), nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    user = relationship("User", back_populates="projects")

    def __repr__(self):
        return f"<Project(id={self.id}, title={self.title})>"
