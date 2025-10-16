"""
Generated CV model for AI-generated CVs.
"""
from sqlalchemy import Column, String, Integer, Boolean, DateTime, ForeignKey, Text
from sqlalchemy.dialects.postgresql import UUID, JSONB, ARRAY
from sqlalchemy.orm import relationship
from datetime import datetime
import uuid

from app.core.database import Base


class GeneratedCV(Base):
    """
    AI-generated CV tailored for specific job applications.
    """
    __tablename__ = "generated_cvs"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(
        UUID(as_uuid=True),
        ForeignKey("auth.users.id", ondelete="CASCADE"),
        nullable=False,
        index=True
    )
    job_id = Column(
        UUID(as_uuid=True),
        ForeignKey("jobs.id", ondelete="SET NULL"),
        nullable=True,
        index=True
    )

    # Content
    content = Column(JSONB, nullable=False)  # Structured CV content
    html_content = Column(Text)  # Rendered HTML
    pdf_url = Column(String(500))  # S3/Storage URL

    # Generation Metadata
    template_id = Column(UUID(as_uuid=True), ForeignKey("cv_templates.id"))
    ai_model = Column(String(50))  # "gpt-4o", "claude-3.5-sonnet"
    generation_params = Column(JSONB)  # Prompt settings, temperature, etc.

    # Selected Content
    included_projects = Column(ARRAY(UUID(as_uuid=True)))  # Which projects were included
    highlighted_skills = Column(ARRAY(Text))  # Which skills were emphasized

    # Versioning
    version = Column(Integer, default=1)
    is_latest = Column(Boolean, default=True)

    # Timestamp
    created_at = Column(DateTime(timezone=True), nullable=False, default=datetime.utcnow)

    # Relationships
    user = relationship("User", back_populates="generated_cvs")
    job = relationship("Job")
    template = relationship("CVTemplate")

    def __repr__(self):
        return f"<GeneratedCV(id={self.id}, user_id={self.user_id}, version={self.version})>"


class CoverLetter(Base):
    """
    AI-generated cover letter for job applications.
    """
    __tablename__ = "cover_letters"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(
        UUID(as_uuid=True),
        ForeignKey("auth.users.id", ondelete="CASCADE"),
        nullable=False,
        index=True
    )
    job_id = Column(
        UUID(as_uuid=True),
        ForeignKey("jobs.id", ondelete="SET NULL"),
        nullable=True,
        index=True
    )

    # Content
    content = Column(Text, nullable=False)
    tone = Column(String(50), default='professional')  # professional, enthusiastic, casual

    # Generation Metadata
    ai_model = Column(String(50))
    generation_params = Column(JSONB)

    # Timestamp
    created_at = Column(DateTime(timezone=True), nullable=False, default=datetime.utcnow)

    # Relationships
    user = relationship("User", back_populates="cover_letters")
    job = relationship("Job")

    def __repr__(self):
        return f"<CoverLetter(id={self.id}, user_id={self.user_id}, tone={self.tone})>"
