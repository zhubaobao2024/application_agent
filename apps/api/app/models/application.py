"""
Application model for tracking job applications.
"""
from sqlalchemy import Column, String, Date, DateTime, ForeignKey, Text, Index
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.orm import relationship
from datetime import datetime
import uuid

from app.core.database import Base


class Application(Base):
    """
    Job application tracking with status and materials.
    """
    __tablename__ = "applications"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(
        UUID(as_uuid=True),
        ForeignKey("auth.users.id", ondelete="CASCADE"),
        nullable=False,
        index=True
    )
    job_id = Column(
        UUID(as_uuid=True),
        ForeignKey("jobs.id", ondelete="CASCADE"),
        nullable=False,
        index=True
    )

    # Status Tracking
    status = Column(
        String(50),
        default='draft',
        nullable=False,
        index=True
    )  # draft, applied, interviewing, offered, rejected, accepted
    applied_at = Column(DateTime(timezone=True))

    # Application Materials
    cv_id = Column(UUID(as_uuid=True), ForeignKey("generated_cvs.id"))
    cover_letter_id = Column(UUID(as_uuid=True), ForeignKey("cover_letters.id"))

    # Notes & Tracking
    notes = Column(Text)
    follow_up_date = Column(Date)
    interview_dates = Column(JSONB)  # Array of interview schedule

    # External Tracking
    external_application_id = Column(String(255))  # If applied through API
    source_applied = Column(String(50))  # "linkedin", "direct", "email"

    # Timestamps
    created_at = Column(DateTime(timezone=True), nullable=False, default=datetime.utcnow)
    updated_at = Column(DateTime(timezone=True), nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    user = relationship("User", back_populates="applications")
    job = relationship("Job", back_populates="applications")
    cv = relationship("GeneratedCV", foreign_keys=[cv_id])
    cover_letter = relationship("CoverLetter", foreign_keys=[cover_letter_id])

    def __repr__(self):
        return f"<Application(id={self.id}, status={self.status})>"


# Create unique constraint on user_id and job_id
Index('idx_applications_user_job', Application.user_id, Application.job_id, unique=True)
