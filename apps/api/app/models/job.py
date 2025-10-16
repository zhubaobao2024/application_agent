"""
Job model for scraped job postings.
"""
from sqlalchemy import Column, String, Integer, Float, Boolean, DateTime, Text, Index
from sqlalchemy.dialects.postgresql import UUID, JSONB, ARRAY
from sqlalchemy.orm import relationship
from datetime import datetime
import uuid

from app.core.database import Base


class Job(Base):
    """
    Job posting scraped from various sources.
    """
    __tablename__ = "jobs"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)

    # Source Information
    external_id = Column(String(255))  # ID from source platform
    source = Column(String(50), nullable=False, index=True)  # "linkedin", "indeed", "greenhouse"
    source_url = Column(String(1000), nullable=False)

    # Job Details
    title = Column(String(255), nullable=False, index=True)
    company = Column(String(255), nullable=False, index=True)
    company_logo_url = Column(String(500))
    location = Column(String(255))
    remote_type = Column(String(50))  # "remote", "hybrid", "onsite"

    # Job Description
    description = Column(Text, nullable=False)
    requirements = Column(Text)
    responsibilities = Column(Text)

    # Compensation
    salary_min = Column(Integer)
    salary_max = Column(Integer)
    salary_currency = Column(String(10), default='USD')
    employment_type = Column(String(50))  # "full-time", "contract", "internship"
    experience_level = Column(String(50))  # "entry", "mid", "senior", "lead"

    # Skills & Benefits
    required_skills = Column(ARRAY(Text))
    preferred_skills = Column(ARRAY(Text))
    benefits = Column(ARRAY(Text))

    # Metadata
    posted_date = Column(DateTime(timezone=True))
    scraped_at = Column(DateTime(timezone=True), nullable=False, default=datetime.utcnow)
    expires_at = Column(DateTime(timezone=True))
    is_active = Column(Boolean, default=True, index=True)

    # AI-Generated Fields
    parsed_requirements = Column(JSONB)  # Structured extraction of requirements
    relevance_score = Column(Float)  # Match score with user profile

    # Timestamps
    created_at = Column(DateTime(timezone=True), nullable=False, default=datetime.utcnow)
    updated_at = Column(DateTime(timezone=True), nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    applications = relationship("Application", back_populates="job")

    def __repr__(self):
        return f"<Job(id={self.id}, title={self.title}, company={self.company})>"


# Create indexes
Index('idx_jobs_external_source', Job.external_id, Job.source, unique=True)
Index('idx_jobs_posted_date', Job.posted_date.desc())
Index('idx_jobs_skills', Job.required_skills, postgresql_using='gin')
Index('idx_jobs_title_company', Job.title, Job.company)

# Full-text search index will be created in migration
# CREATE INDEX idx_jobs_fts ON jobs USING GIN(
#   to_tsvector('english', title || ' ' || company || ' ' || description)
# );
