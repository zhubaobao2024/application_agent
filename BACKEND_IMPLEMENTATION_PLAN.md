# Backend Implementation Plan

**Project:** AI Job Application Assistant - Backend Services
**Tech Stack:** FastAPI (Python), PostgreSQL, Redis, Celery, OpenAI/Anthropic APIs
**Target Timeline:** 8-10 weeks (MVP)
**Last Updated:** 2025-10-15

---

## Table of Contents
1. [Phase 0: Setup & Infrastructure](#phase-0-setup--infrastructure)
2. [Phase 1: Core Database & Authentication](#phase-1-core-database--authentication)
3. [Phase 2: User Profile & Projects Management](#phase-2-user-profile--projects-management)
4. [Phase 3: AI Integration Layer](#phase-3-ai-integration-layer)
5. [Phase 4: Job Scraping System](#phase-4-job-scraping-system)
6. [Phase 5: Application Management](#phase-5-application-management)
7. [Phase 6: Testing & Optimization](#phase-6-testing--optimization)
8. [Phase 7: Deployment & Monitoring](#phase-7-deployment--monitoring)

---

## Phase 0: Setup & Infrastructure
**Duration:** Week 1 (5-7 days)
**Priority:** Critical

### Tasks

#### 1. Project Structure Setup
```bash
application_agent/
├── apps/
│   └── api/
│       ├── app/
│       │   ├── __init__.py
│       │   ├── main.py                 # FastAPI app initialization
│       │   ├── config.py               # Configuration management
│       │   ├── dependencies.py         # Dependency injection
│       │   │
│       │   ├── api/                    # API layer
│       │   │   ├── __init__.py
│       │   │   ├── v1/
│       │   │   │   ├── __init__.py
│       │   │   │   ├── routes/
│       │   │   │   │   ├── auth.py
│       │   │   │   │   ├── profile.py
│       │   │   │   │   ├── projects.py
│       │   │   │   │   ├── jobs.py
│       │   │   │   │   ├── applications.py
│       │   │   │   │   └── cvs.py
│       │   │   │   └── deps.py         # Route dependencies
│       │   │
│       │   ├── core/                   # Core functionality
│       │   │   ├── __init__.py
│       │   │   ├── security.py         # JWT, hashing
│       │   │   ├── database.py         # Database connection
│       │   │   ├── cache.py            # Redis cache
│       │   │   └── exceptions.py       # Custom exceptions
│       │   │
│       │   ├── models/                 # SQLAlchemy models
│       │   │   ├── __init__.py
│       │   │   ├── user.py
│       │   │   ├── profile.py
│       │   │   ├── project.py
│       │   │   ├── job.py
│       │   │   ├── application.py
│       │   │   └── cv.py
│       │   │
│       │   ├── schemas/                # Pydantic schemas
│       │   │   ├── __init__.py
│       │   │   ├── user.py
│       │   │   ├── profile.py
│       │   │   ├── project.py
│       │   │   ├── job.py
│       │   │   ├── application.py
│       │   │   └── cv.py
│       │   │
│       │   ├── services/               # Business logic
│       │   │   ├── __init__.py
│       │   │   ├── ai/
│       │   │   │   ├── __init__.py
│       │   │   │   ├── providers.py    # AI provider abstraction
│       │   │   │   ├── cv_generator.py
│       │   │   │   ├── cover_letter.py
│       │   │   │   └── analyzer.py
│       │   │   ├── scraper/
│       │   │   │   ├── __init__.py
│       │   │   │   ├── base.py
│       │   │   │   ├── linkedin.py
│       │   │   │   ├── indeed.py
│       │   │   │   └── greenhouse.py
│       │   │   └── parser/
│       │   │       ├── __init__.py
│       │   │       └── cv_parser.py
│       │   │
│       │   ├── tasks/                  # Celery tasks
│       │   │   ├── __init__.py
│       │   │   ├── celery_app.py
│       │   │   ├── scraping.py
│       │   │   └── ai_generation.py
│       │   │
│       │   └── utils/                  # Utilities
│       │       ├── __init__.py
│       │       ├── logger.py
│       │       ├── validators.py
│       │       └── helpers.py
│       │
│       ├── alembic/                    # Database migrations
│       │   ├── versions/
│       │   ├── env.py
│       │   └── alembic.ini
│       │
│       ├── tests/
│       │   ├── __init__.py
│       │   ├── conftest.py
│       │   ├── test_api/
│       │   ├── test_services/
│       │   └── test_models/
│       │
│       ├── pyproject.toml              # Poetry configuration
│       ├── poetry.lock
│       ├── .env.example
│       ├── .env
│       ├── Dockerfile
│       └── docker-compose.yml
```

#### 2. Initialize Poetry Project
```bash
cd apps/api
poetry init
poetry add fastapi uvicorn[standard]
poetry add sqlalchemy alembic psycopg2-binary
poetry add pydantic pydantic-settings
poetry add python-jose[cryptography] passlib[bcrypt]
poetry add redis celery
poetry add openai anthropic langchain tiktoken
poetry add playwright beautifulsoup4 requests
poetry add python-multipart aiofiles
poetry add sentry-sdk python-dotenv

# Dev dependencies
poetry add --group dev pytest pytest-asyncio pytest-cov
poetry add --group dev black isort mypy
poetry add --group dev httpx
```

#### 3. Environment Configuration
Create `app/config.py`:
```python
from pydantic_settings import BaseSettings
from typing import Optional

class Settings(BaseSettings):
    # App
    PROJECT_NAME: str = "Job Application AI"
    VERSION: str = "1.0.0"
    API_V1_PREFIX: str = "/api/v1"
    DEBUG: bool = False

    # Database
    DATABASE_URL: str
    DB_POOL_SIZE: int = 10
    DB_MAX_OVERFLOW: int = 20

    # Redis
    REDIS_URL: str = "redis://localhost:6379/0"

    # Supabase
    SUPABASE_URL: str
    SUPABASE_ANON_KEY: str
    SUPABASE_SERVICE_KEY: str

    # JWT
    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60

    # AI Services
    OPENAI_API_KEY: str
    ANTHROPIC_API_KEY: Optional[str] = None
    AI_DEFAULT_MODEL: str = "gpt-4o"
    AI_FALLBACK_MODEL: str = "claude-3-5-sonnet-20241022"

    # Job Scraping
    LINKEDIN_EMAIL: Optional[str] = None
    LINKEDIN_PASSWORD: Optional[str] = None
    INDEED_API_KEY: Optional[str] = None

    # Storage
    AWS_ACCESS_KEY_ID: Optional[str] = None
    AWS_SECRET_ACCESS_KEY: Optional[str] = None
    AWS_S3_BUCKET: Optional[str] = None
    AWS_REGION: str = "us-east-1"

    # Monitoring
    SENTRY_DSN: Optional[str] = None

    # Rate Limiting
    RATE_LIMIT_PER_MINUTE: int = 60

    class Config:
        env_file = ".env"
        case_sensitive = True

settings = Settings()
```

#### 4. Docker Setup
Create `docker-compose.yml`:
```yaml
version: '3.8'

services:
  postgres:
    image: postgres:15-alpine
    environment:
      POSTGRES_DB: job_app_dev
      POSTGRES_USER: postgres
      POSTGRES_PASSWORD: postgres
    ports:
      - "5432:5432"
    volumes:
      - postgres_data:/var/lib/postgresql/data

  redis:
    image: redis:7-alpine
    ports:
      - "6379:6379"
    volumes:
      - redis_data:/data

  api:
    build: .
    command: uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
    volumes:
      - .:/app
    ports:
      - "8000:8000"
    env_file:
      - .env
    depends_on:
      - postgres
      - redis

  celery_worker:
    build: .
    command: celery -A app.tasks.celery_app worker --loglevel=info
    volumes:
      - .:/app
    env_file:
      - .env
    depends_on:
      - postgres
      - redis

  celery_beat:
    build: .
    command: celery -A app.tasks.celery_app beat --loglevel=info
    volumes:
      - .:/app
    env_file:
      - .env
    depends_on:
      - postgres
      - redis

volumes:
  postgres_data:
  redis_data:
```

#### 5. FastAPI Main Application
Create `app/main.py`:
```python
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.config import settings
from app.api.v1.routes import auth, profile, projects, jobs, applications, cvs

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    openapi_url=f"{settings.API_V1_PREFIX}/openapi.json"
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(auth.router, prefix=f"{settings.API_V1_PREFIX}/auth", tags=["auth"])
app.include_router(profile.router, prefix=f"{settings.API_V1_PREFIX}/profile", tags=["profile"])
app.include_router(projects.router, prefix=f"{settings.API_V1_PREFIX}/projects", tags=["projects"])
app.include_router(jobs.router, prefix=f"{settings.API_V1_PREFIX}/jobs", tags=["jobs"])
app.include_router(applications.router, prefix=f"{settings.API_V1_PREFIX}/applications", tags=["applications"])
app.include_router(cvs.router, prefix=f"{settings.API_V1_PREFIX}/cvs", tags=["cvs"])

@app.get("/")
async def root():
    return {"message": "Job Application AI API", "version": settings.VERSION}

@app.get("/health")
async def health_check():
    return {"status": "healthy"}
```

**Deliverables:**
- [ ] Project structure created
- [ ] Poetry dependencies installed
- [ ] Configuration management setup
- [ ] Docker Compose running locally
- [ ] FastAPI app responding to health checks

---

## Phase 1: Core Database & Authentication
**Duration:** Week 2 (5-7 days)
**Priority:** Critical

### Tasks

#### 1. Database Connection Setup
Create `app/core/database.py`:
```python
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from app.config import settings

engine = create_engine(
    settings.DATABASE_URL,
    pool_size=settings.DB_POOL_SIZE,
    max_overflow=settings.DB_MAX_OVERFLOW,
    pool_pre_ping=True,
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
```

#### 2. Database Models
Create models following the schema in DESIGN.md:

**`app/models/user.py`** (Supabase manages this, but we'll create a reference):
```python
from sqlalchemy import Column, String, DateTime, Boolean
from sqlalchemy.dialects.postgresql import UUID
from app.core.database import Base
import uuid

class User(Base):
    __tablename__ = "users"
    __table_args__ = {'schema': 'auth'}

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    email = Column(String, unique=True, nullable=False, index=True)
    email_confirmed_at = Column(DateTime, nullable=True)
    created_at = Column(DateTime, nullable=False)
```

**`app/models/profile.py`**:
```python
from sqlalchemy import Column, String, Integer, Boolean, DateTime, ForeignKey, Text, ARRAY
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.orm import relationship
from app.core.database import Base
import uuid
from datetime import datetime

class UserProfile(Base):
    __tablename__ = "user_profiles"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("auth.users.id", ondelete="CASCADE"), unique=True)

    full_name = Column(String(255), nullable=False)
    phone = Column(String(50))
    location = Column(String(255))
    linkedin_url = Column(String(500))
    github_url = Column(String(500))
    portfolio_url = Column(String(500))

    # Preferences
    target_roles = Column(ARRAY(Text))
    preferred_locations = Column(ARRAY(Text))
    desired_salary_min = Column(Integer)
    desired_salary_max = Column(Integer)
    willing_to_relocate = Column(Boolean, default=False)

    # Base CV content
    summary = Column(Text)
    skills = Column(JSONB)
    education = Column(JSONB)
    work_experience = Column(JSONB)

    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    projects = relationship("Project", back_populates="user", cascade="all, delete-orphan")
```

**`app/models/project.py`**:
```python
from sqlalchemy import Column, String, Date, Boolean, DateTime, ForeignKey, Text, ARRAY
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.orm import relationship
from app.core.database import Base
import uuid
from datetime import datetime

class Project(Base):
    __tablename__ = "projects"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("auth.users.id", ondelete="CASCADE"))

    title = Column(String(255), nullable=False)
    description = Column(Text)
    detailed_description = Column(Text)
    technologies = Column(ARRAY(Text))

    role = Column(String(100))
    start_date = Column(Date)
    end_date = Column(Date, nullable=True)

    github_url = Column(String(500))
    demo_url = Column(String(500))

    achievements = Column(ARRAY(Text))
    metrics = Column(JSONB)

    is_featured = Column(Boolean, default=False)
    relevance_tags = Column(ARRAY(Text))

    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    user = relationship("UserProfile", back_populates="projects")
```

#### 3. Alembic Migrations
```bash
# Initialize Alembic
poetry run alembic init alembic

# Create initial migration
poetry run alembic revision --autogenerate -m "Initial database schema"

# Apply migration
poetry run alembic upgrade head
```

#### 4. Authentication with Supabase
Create `app/core/security.py`:
```python
from datetime import datetime, timedelta
from typing import Optional
from jose import JWTError, jwt
from passlib.context import CryptContext
from app.config import settings

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=15))
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return encoded_jwt

def verify_token(token: str) -> Optional[dict]:
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        return payload
    except JWTError:
        return None
```

#### 5. Pydantic Schemas
Create `app/schemas/user.py`:
```python
from pydantic import BaseModel, EmailStr, UUID4
from typing import Optional
from datetime import datetime

class UserBase(BaseModel):
    email: EmailStr

class UserCreate(UserBase):
    password: str
    full_name: str

class UserLogin(UserBase):
    password: str

class UserResponse(UserBase):
    id: UUID4
    email_confirmed: bool

    class Config:
        from_attributes = True

class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"
    expires_at: datetime

class TokenData(BaseModel):
    user_id: Optional[UUID4] = None
```

**Deliverables:**
- [ ] Database models created for all entities
- [ ] Alembic migrations setup and tested
- [ ] Authentication utilities implemented
- [ ] Pydantic schemas for request/response validation
- [ ] Database connection pooling working

---

## Phase 2: User Profile & Projects Management
**Duration:** Week 3 (5-7 days)
**Priority:** High

### Tasks

#### 1. Profile API Endpoints
Create `app/api/v1/routes/profile.py`:
```python
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.schemas.profile import ProfileResponse, ProfileUpdate
from app.models.profile import UserProfile
from app.api.v1.deps import get_current_user

router = APIRouter()

@router.get("/", response_model=ProfileResponse)
async def get_profile(
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get current user's profile"""
    profile = db.query(UserProfile).filter(
        UserProfile.user_id == current_user["id"]
    ).first()

    if not profile:
        raise HTTPException(status_code=404, detail="Profile not found")

    return profile

@router.put("/", response_model=ProfileResponse)
async def update_profile(
    profile_data: ProfileUpdate,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Update user profile"""
    profile = db.query(UserProfile).filter(
        UserProfile.user_id == current_user["id"]
    ).first()

    if not profile:
        raise HTTPException(status_code=404, detail="Profile not found")

    for key, value in profile_data.dict(exclude_unset=True).items():
        setattr(profile, key, value)

    db.commit()
    db.refresh(profile)
    return profile
```

#### 2. Projects API Endpoints
Create `app/api/v1/routes/projects.py`:
```python
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.core.database import get_db
from app.schemas.project import ProjectCreate, ProjectUpdate, ProjectResponse
from app.models.project import Project
from app.api.v1.deps import get_current_user

router = APIRouter()

@router.get("/", response_model=List[ProjectResponse])
async def list_projects(
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """List all user projects"""
    projects = db.query(Project).filter(
        Project.user_id == current_user["id"]
    ).all()
    return projects

@router.post("/", response_model=ProjectResponse, status_code=201)
async def create_project(
    project_data: ProjectCreate,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Create a new project"""
    project = Project(**project_data.dict(), user_id=current_user["id"])
    db.add(project)
    db.commit()
    db.refresh(project)
    return project

@router.put("/{project_id}", response_model=ProjectResponse)
async def update_project(
    project_id: str,
    project_data: ProjectUpdate,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Update a project"""
    project = db.query(Project).filter(
        Project.id == project_id,
        Project.user_id == current_user["id"]
    ).first()

    if not project:
        raise HTTPException(status_code=404, detail="Project not found")

    for key, value in project_data.dict(exclude_unset=True).items():
        setattr(project, key, value)

    db.commit()
    db.refresh(project)
    return project

@router.delete("/{project_id}")
async def delete_project(
    project_id: str,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Delete a project"""
    project = db.query(Project).filter(
        Project.id == project_id,
        Project.user_id == current_user["id"]
    ).first()

    if not project:
        raise HTTPException(status_code=404, detail="Project not found")

    db.delete(project)
    db.commit()
    return {"success": True}
```

#### 3. Authentication Dependency
Create `app/api/v1/deps.py`:
```python
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from app.core.security import verify_token

security = HTTPBearer()

async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security)
) -> dict:
    """Verify JWT token and return user data"""
    token = credentials.credentials
    payload = verify_token(token)

    if payload is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials"
        )

    return payload
```

**Deliverables:**
- [ ] Profile CRUD endpoints implemented
- [ ] Projects CRUD endpoints implemented
- [ ] JWT authentication middleware working
- [ ] API tested with Postman/curl
- [ ] Unit tests for profile and projects

---

## Phase 3: AI Integration Layer
**Duration:** Week 4-5 (10-12 days)
**Priority:** Critical

### Tasks

#### 1. AI Provider Abstraction
Create `app/services/ai/providers.py`:
```python
from abc import ABC, abstractmethod
from typing import Optional, Dict, Any
import openai
import anthropic
from app.config import settings

class AIProvider(ABC):
    @abstractmethod
    async def generate_completion(
        self,
        prompt: str,
        **kwargs
    ) -> str:
        pass

class OpenAIProvider(AIProvider):
    def __init__(self):
        self.client = openai.AsyncOpenAI(api_key=settings.OPENAI_API_KEY)

    async def generate_completion(
        self,
        prompt: str,
        model: str = "gpt-4o",
        temperature: float = 0.7,
        max_tokens: int = 2000,
        **kwargs
    ) -> Dict[str, Any]:
        response = await self.client.chat.completions.create(
            model=model,
            messages=[{"role": "user", "content": prompt}],
            temperature=temperature,
            max_tokens=max_tokens,
            **kwargs
        )

        return {
            "content": response.choices[0].message.content,
            "tokens": {
                "input": response.usage.prompt_tokens,
                "output": response.usage.completion_tokens
            },
            "model": model
        }

class AnthropicProvider(AIProvider):
    def __init__(self):
        self.client = anthropic.AsyncAnthropic(api_key=settings.ANTHROPIC_API_KEY)

    async def generate_completion(
        self,
        prompt: str,
        model: str = "claude-3-5-sonnet-20241022",
        temperature: float = 0.7,
        max_tokens: int = 2000,
        **kwargs
    ) -> Dict[str, Any]:
        response = await self.client.messages.create(
            model=model,
            messages=[{"role": "user", "content": prompt}],
            temperature=temperature,
            max_tokens=max_tokens,
            **kwargs
        )

        return {
            "content": response.content[0].text,
            "tokens": {
                "input": response.usage.input_tokens,
                "output": response.usage.output_tokens
            },
            "model": model
        }

async def generate_with_fallback(prompt: str, **kwargs) -> Dict[str, Any]:
    """Generate with primary provider, fallback to secondary on failure"""
    try:
        provider = OpenAIProvider()
        return await provider.generate_completion(prompt, **kwargs)
    except Exception as e:
        print(f"OpenAI failed: {e}, trying Anthropic")
        if settings.ANTHROPIC_API_KEY:
            provider = AnthropicProvider()
            return await provider.generate_completion(prompt, **kwargs)
        raise
```

#### 2. CV Generation Service
Create `app/services/ai/cv_generator.py`:
```python
from typing import Dict, Any, List, Optional
from app.services.ai.providers import generate_with_fallback
from app.models.profile import UserProfile
from app.models.project import Project
from app.models.job import Job
import json

CV_GENERATION_PROMPT = """
You are an expert CV writer. Generate a tailored CV for the following job posting.

USER PROFILE:
{user_profile}

PROJECTS:
{projects}

JOB POSTING:
Title: {job_title}
Company: {job_company}
Description: {job_description}
Requirements: {job_requirements}

INSTRUCTIONS:
1. Emphasize skills and projects most relevant to this role
2. Use metrics and quantifiable achievements where possible
3. Match the tone and keywords from the job description
4. Keep descriptions concise (2-3 bullet points per experience)
5. Highlight {emphasize_skills} if present in the user's background

OUTPUT FORMAT:
Return a JSON object with the following structure:
{{
  "summary": "Professional summary (3-4 sentences)",
  "experience": [...],
  "projects": [...],
  "skills": {{...}},
  "education": [...]
}}
"""

class CVGenerator:
    async def generate_cv(
        self,
        user_profile: UserProfile,
        projects: List[Project],
        job: Job,
        options: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Generate tailored CV for a job"""

        # Build prompt
        prompt = CV_GENERATION_PROMPT.format(
            user_profile=self._format_profile(user_profile),
            projects=self._format_projects(projects),
            job_title=job.title,
            job_company=job.company,
            job_description=job.description,
            job_requirements=job.requirements or "",
            emphasize_skills=", ".join(options.get("emphasize_skills", []))
        )

        # Generate with AI
        result = await generate_with_fallback(
            prompt,
            temperature=0.7,
            max_tokens=2000
        )

        # Parse response
        cv_content = json.loads(result["content"])

        return {
            "content": cv_content,
            "tokens_used": result["tokens"],
            "model": result["model"]
        }

    def _format_profile(self, profile: UserProfile) -> str:
        return f"""
Name: {profile.full_name}
Summary: {profile.summary}
Skills: {json.dumps(profile.skills)}
Work Experience: {json.dumps(profile.work_experience)}
Education: {json.dumps(profile.education)}
"""

    def _format_projects(self, projects: List[Project]) -> str:
        return json.dumps([
            {
                "title": p.title,
                "description": p.detailed_description,
                "technologies": p.technologies,
                "achievements": p.achievements,
                "metrics": p.metrics
            }
            for p in projects
        ], indent=2)
```

#### 3. Cover Letter Generation Service
Create `app/services/ai/cover_letter.py`:
```python
from typing import Dict, Any
from app.services.ai.providers import generate_with_fallback
from app.models.profile import UserProfile
from app.models.job import Job

COVER_LETTER_PROMPT = """
You are an expert cover letter writer. Generate a compelling cover letter.

USER PROFILE:
Name: {user_name}
Background: {user_summary}
Key Projects: {key_projects}

JOB:
Title: {job_title}
Company: {job_company}
Description: {job_description}

TONE: {tone} (professional/enthusiastic/casual)

INSTRUCTIONS:
1. Opening: Express genuine interest in the role and company
2. Body (2-3 paragraphs):
   - Highlight most relevant experience
   - Connect past projects to job requirements
   - Show understanding of company's mission
3. Closing: Call to action and gratitude

LENGTH: 250-350 words

Generate the cover letter:
"""

class CoverLetterGenerator:
    async def generate_cover_letter(
        self,
        user_profile: UserProfile,
        job: Job,
        tone: str = "professional",
        key_points: List[str] = None
    ) -> Dict[str, Any]:
        """Generate cover letter for a job"""

        prompt = COVER_LETTER_PROMPT.format(
            user_name=user_profile.full_name,
            user_summary=user_profile.summary,
            key_projects=", ".join(key_points or []),
            job_title=job.title,
            job_company=job.company,
            job_description=job.description,
            tone=tone
        )

        result = await generate_with_fallback(
            prompt,
            temperature=0.8,
            max_tokens=1000
        )

        return {
            "content": result["content"],
            "tokens_used": result["tokens"],
            "model": result["model"]
        }
```

#### 4. AI API Endpoints
Create `app/api/v1/routes/ai.py`:
```python
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.schemas.ai import CVGenerateRequest, CVGenerateResponse, CoverLetterRequest, CoverLetterResponse
from app.services.ai.cv_generator import CVGenerator
from app.services.ai.cover_letter import CoverLetterGenerator
from app.api.v1.deps import get_current_user
from app.models.profile import UserProfile
from app.models.project import Project
from app.models.job import Job
from app.models.cv import GeneratedCV
from app.models.cover_letter import CoverLetter
import time

router = APIRouter()

@router.post("/cv/generate", response_model=CVGenerateResponse, status_code=201)
async def generate_cv(
    request: CVGenerateRequest,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Generate tailored CV for a job"""
    start_time = time.time()

    # Get user profile
    profile = db.query(UserProfile).filter(
        UserProfile.user_id == current_user["id"]
    ).first()

    if not profile:
        raise HTTPException(status_code=404, detail="Profile not found")

    # Get job
    job = db.query(Job).filter(Job.id == request.job_id).first()
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")

    # Get projects
    projects = db.query(Project).filter(
        Project.user_id == current_user["id"]
    ).all()

    if request.options.include_projects:
        projects = [p for p in projects if str(p.id) in request.options.include_projects]

    # Generate CV
    generator = CVGenerator()
    result = await generator.generate_cv(profile, projects, job, request.options.dict())

    # Save to database
    cv = GeneratedCV(
        user_id=current_user["id"],
        job_id=request.job_id,
        template_id=request.template_id,
        content=result["content"],
        ai_model=result["model"],
        generation_params=request.options.dict(),
        included_projects=[str(p.id) for p in projects],
        highlighted_skills=request.options.emphasize_skills or []
    )
    db.add(cv)
    db.commit()
    db.refresh(cv)

    generation_time = int((time.time() - start_time) * 1000)

    return {
        "cv_id": cv.id,
        "content": result["content"],
        "pdf_url": f"/api/v1/cvs/{cv.id}/download",  # TODO: Implement PDF generation
        "generation_time_ms": generation_time,
        "tokens_used": result["tokens_used"],
        "estimated_cost": calculate_cost(result["tokens_used"])
    }

@router.post("/cover-letter/generate", response_model=CoverLetterResponse, status_code=201)
async def generate_cover_letter(
    request: CoverLetterRequest,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Generate cover letter for a job"""
    start_time = time.time()

    # Get user profile
    profile = db.query(UserProfile).filter(
        UserProfile.user_id == current_user["id"]
    ).first()

    if not profile:
        raise HTTPException(status_code=404, detail="Profile not found")

    # Get job
    job = db.query(Job).filter(Job.id == request.job_id).first()
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")

    # Generate cover letter
    generator = CoverLetterGenerator()
    result = await generator.generate_cover_letter(
        profile, job, request.tone, request.key_points
    )

    # Save to database
    cover_letter = CoverLetter(
        user_id=current_user["id"],
        job_id=request.job_id,
        content=result["content"],
        tone=request.tone,
        ai_model=result["model"],
        generation_params={"key_points": request.key_points}
    )
    db.add(cover_letter)
    db.commit()
    db.refresh(cover_letter)

    generation_time = int((time.time() - start_time) * 1000)

    return {
        "cover_letter_id": cover_letter.id,
        "content": result["content"],
        "generation_time_ms": generation_time,
        "tokens_used": result["tokens_used"],
        "estimated_cost": calculate_cost(result["tokens_used"])
    }

def calculate_cost(tokens: dict) -> float:
    """Calculate estimated cost based on token usage"""
    # GPT-4o pricing: $2.50 / 1M input, $10 / 1M output
    input_cost = (tokens["input"] / 1_000_000) * 2.50
    output_cost = (tokens["output"] / 1_000_000) * 10.0
    return round(input_cost + output_cost, 4)
```

**Deliverables:**
- [ ] AI provider abstraction with fallback
- [ ] CV generation service with prompt engineering
- [ ] Cover letter generation service
- [ ] AI API endpoints tested
- [ ] Token usage tracking and cost estimation
- [ ] Unit tests for AI services

---

## Phase 4: Job Scraping System
**Duration:** Week 5-6 (10-12 days)
**Priority:** High

### Tasks

#### 1. Job Model
Create `app/models/job.py`:
```python
from sqlalchemy import Column, String, Integer, Boolean, DateTime, Float, Text, ARRAY
from sqlalchemy.dialects.postgresql import UUID, JSONB
from app.core.database import Base
import uuid
from datetime import datetime

class Job(Base):
    __tablename__ = "jobs"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)

    external_id = Column(String(255))
    source = Column(String(50), nullable=False)
    source_url = Column(String(1000), nullable=False)

    title = Column(String(255), nullable=False)
    company = Column(String(255), nullable=False)
    company_logo_url = Column(String(500))
    location = Column(String(255))
    remote_type = Column(String(50))

    description = Column(Text, nullable=False)
    requirements = Column(Text)
    responsibilities = Column(Text)

    salary_min = Column(Integer)
    salary_max = Column(Integer)
    salary_currency = Column(String(10), default='USD')
    employment_type = Column(String(50))
    experience_level = Column(String(50))

    required_skills = Column(ARRAY(Text))
    preferred_skills = Column(ARRAY(Text))
    benefits = Column(ARRAY(Text))

    posted_date = Column(DateTime)
    scraped_at = Column(DateTime, default=datetime.utcnow)
    expires_at = Column(DateTime)
    is_active = Column(Boolean, default=True)

    parsed_requirements = Column(JSONB)
    relevance_score = Column(Float)

    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
```

#### 2. Base Scraper
Create `app/services/scraper/base.py`:
```python
from abc import ABC, abstractmethod
from typing import List, Dict, Any
from dataclasses import dataclass
import asyncio
import random

@dataclass
class SearchParams:
    roles: List[str]
    locations: List[str]
    experience_level: List[str]
    min_salary: int = None
    remote_only: bool = False
    max_results: int = 100

@dataclass
class RawJob:
    external_id: str
    source: str
    source_url: str
    title: str
    company: str
    location: str
    description: str
    requirements: str = None
    posted_date: str = None

class RateLimiter:
    def __init__(self, requests_per_hour: int):
        self.delay = 3600 / requests_per_hour

    async def wait(self):
        await asyncio.sleep(self.delay + random.uniform(0, 2))

class JobScraper(ABC):
    def __init__(self):
        self.rate_limiter = RateLimiter(50)

    @abstractmethod
    async def scrape_jobs(
        self,
        search_params: SearchParams
    ) -> List[RawJob]:
        pass

    def build_search_url(self, params: SearchParams) -> str:
        """Build search URL from parameters"""
        pass
```

#### 3. LinkedIn Scraper
Create `app/services/scraper/linkedin.py`:
```python
from typing import List
from playwright.async_api import async_playwright
from app.services.scraper.base import JobScraper, SearchParams, RawJob
import os

class LinkedInScraper(JobScraper):
    async def scrape_jobs(self, params: SearchParams) -> List[RawJob]:
        """Scrape jobs from LinkedIn"""
        results = []

        async with async_playwright() as p:
            browser = await p.chromium.launch(headless=True)
            context = await browser.new_context(
                user_agent="Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36"
            )
            page = await context.new_page()

            # Login
            await self._login(page)

            # Search for each role
            for role in params.roles:
                for location in params.locations:
                    search_url = self._build_search_url(role, location, params)
                    await page.goto(search_url)
                    await page.wait_for_selector(".job-card-list")

                    # Extract job cards
                    job_cards = await page.query_selector_all(".job-card-container")

                    for card in job_cards[:params.max_results]:
                        await self.rate_limiter.wait()
                        job_data = await self._extract_job_data(page, card)
                        if job_data:
                            results.append(job_data)

            await browser.close()

        return results

    async def _login(self, page):
        """Login to LinkedIn"""
        await page.goto("https://www.linkedin.com/login")
        await page.fill("#username", os.getenv("LINKEDIN_EMAIL"))
        await page.fill("#password", os.getenv("LINKEDIN_PASSWORD"))
        await page.click("[type=submit]")
        await page.wait_for_url("https://www.linkedin.com/feed/")

    def _build_search_url(self, role: str, location: str, params: SearchParams) -> str:
        """Build LinkedIn search URL"""
        base_url = "https://www.linkedin.com/jobs/search/"
        query_params = {
            "keywords": role,
            "location": location,
            "f_TPR": "r86400",  # Past 24 hours
        }

        if params.remote_only:
            query_params["f_WT"] = "2"  # Remote

        query_string = "&".join([f"{k}={v}" for k, v in query_params.items()])
        return f"{base_url}?{query_string}"

    async def _extract_job_data(self, page, card) -> RawJob:
        """Extract job data from card"""
        try:
            # Click on card to load details
            await card.click()
            await page.wait_for_selector(".job-details")

            title = await page.locator(".job-details__title").text_content()
            company = await page.locator(".job-details__company-name").text_content()
            location = await page.locator(".job-details__location").text_content()
            description = await page.locator(".job-details__description").text_content()

            job_link = await card.locator("a").get_attribute("href")
            job_id = job_link.split("/")[-1].split("?")[0]

            return RawJob(
                external_id=f"linkedin_{job_id}",
                source="linkedin",
                source_url=f"https://www.linkedin.com/jobs/view/{job_id}",
                title=title.strip(),
                company=company.strip(),
                location=location.strip(),
                description=description.strip()
            )
        except Exception as e:
            print(f"Error extracting job: {e}")
            return None
```

#### 4. Celery Task for Scraping
Create `app/tasks/scraping.py`:
```python
from celery import Task
from app.tasks.celery_app import celery_app
from app.services.scraper.linkedin import LinkedInScraper
from app.services.scraper.indeed import IndeedScraper
from app.services.scraper.base import SearchParams
from app.core.database import SessionLocal
from app.models.job import Job
from typing import Dict, Any
import asyncio

@celery_app.task(bind=True, name="scrape_jobs")
def scrape_jobs_task(
    self: Task,
    user_id: str,
    sources: list[str],
    preferences: Dict[str, Any]
) -> Dict[str, Any]:
    """Celery task to scrape jobs from multiple sources"""

    # Build search params
    search_params = SearchParams(
        roles=preferences.get("roles", []),
        locations=preferences.get("locations", []),
        experience_level=preferences.get("experience_level", []),
        min_salary=preferences.get("min_salary"),
        max_results=preferences.get("max_results", 100)
    )

    results = {
        "jobs_found": 0,
        "jobs_saved": 0,
        "jobs_skipped": 0,
        "by_source": {}
    }

    db = SessionLocal()

    try:
        for source in sources:
            self.update_state(state="PROGRESS", meta={"source": source})

            # Select scraper
            if source == "linkedin":
                scraper = LinkedInScraper()
            elif source == "indeed":
                scraper = IndeedScraper()
            else:
                continue

            # Scrape jobs
            raw_jobs = asyncio.run(scraper.scrape_jobs(search_params))

            source_results = {"found": len(raw_jobs), "saved": 0, "skipped": 0}

            # Save to database
            for raw_job in raw_jobs:
                results["jobs_found"] += 1

                # Check if exists
                existing = db.query(Job).filter(
                    Job.external_id == raw_job.external_id,
                    Job.source == raw_job.source
                ).first()

                if existing:
                    source_results["skipped"] += 1
                    results["jobs_skipped"] += 1
                    continue

                # Create job
                job = Job(
                    external_id=raw_job.external_id,
                    source=raw_job.source,
                    source_url=raw_job.source_url,
                    title=raw_job.title,
                    company=raw_job.company,
                    location=raw_job.location,
                    description=raw_job.description,
                    requirements=raw_job.requirements
                )
                db.add(job)
                source_results["saved"] += 1
                results["jobs_saved"] += 1

            results["by_source"][source] = source_results
            db.commit()

    finally:
        db.close()

    return results
```

#### 5. Scraper API Endpoints
Create `app/api/v1/routes/scraper.py`:
```python
from fastapi import APIRouter, Depends
from app.schemas.scraper import ScraperTriggerRequest, ScraperStatusResponse
from app.tasks.scraping import scrape_jobs_task
from app.api.v1.deps import get_current_user

router = APIRouter()

@router.post("/trigger", status_code=202)
async def trigger_scraping(
    request: ScraperTriggerRequest,
    current_user: dict = Depends(get_current_user)
):
    """Trigger job scraping task"""

    task = scrape_jobs_task.delay(
        user_id=current_user["id"],
        sources=request.sources,
        preferences=request.preferences.dict()
    )

    return {
        "job_id": task.id,
        "status": "queued",
        "estimated_duration": len(request.sources) * 60
    }

@router.get("/status/{job_id}", response_model=ScraperStatusResponse)
async def get_scraping_status(job_id: str):
    """Check status of scraping job"""

    task = scrape_jobs_task.AsyncResult(job_id)

    if task.state == "PENDING":
        return {"job_id": job_id, "status": "queued"}

    elif task.state == "PROGRESS":
        return {
            "job_id": job_id,
            "status": "in_progress",
            "progress": task.info
        }

    elif task.state == "SUCCESS":
        return {
            "job_id": job_id,
            "status": "completed",
            "results": task.result
        }

    else:
        return {
            "job_id": job_id,
            "status": "failed",
            "error": str(task.info)
        }
```

**Deliverables:**
- [ ] Base scraper interface
- [ ] LinkedIn scraper with Playwright
- [ ] Indeed scraper (or another source)
- [ ] Celery tasks for async scraping
- [ ] Scraper API endpoints
- [ ] Deduplication logic
- [ ] Rate limiting and anti-bot measures

---

## Phase 5: Application Management
**Duration:** Week 7 (5-7 days)
**Priority:** Medium

### Tasks

#### 1. Application Models
Create the remaining models for applications, generated CVs, and cover letters following the schema in DESIGN.md.

#### 2. Jobs API
Create `app/api/v1/routes/jobs.py` with:
- List jobs (with pagination, filtering)
- Get job details
- Search jobs
- Favorite/hide jobs

#### 3. Applications API
Create `app/api/v1/routes/applications.py` with:
- List applications
- Create application
- Update application status
- Delete application

#### 4. CVs API
Create `app/api/v1/routes/cvs.py` with:
- List generated CVs
- Get CV details
- Download CV as PDF

**Deliverables:**
- [ ] Jobs CRUD endpoints
- [ ] Applications CRUD endpoints
- [ ] CVs listing and download
- [ ] Pagination and filtering
- [ ] Unit tests

---

## Phase 6: Testing & Optimization
**Duration:** Week 8 (5-7 days)
**Priority:** High

### Tasks

#### 1. Unit Tests
```python
# tests/test_services/test_ai_generator.py
import pytest
from app.services.ai.cv_generator import CVGenerator

@pytest.mark.asyncio
async def test_cv_generation(mock_profile, mock_job):
    generator = CVGenerator()
    result = await generator.generate_cv(mock_profile, [], mock_job, {})
    assert "content" in result
    assert "tokens_used" in result
```

#### 2. Integration Tests
Test end-to-end flows:
- User signup → create profile → generate CV
- Trigger scraping → list jobs → create application

#### 3. Performance Optimization
- Add Redis caching for job listings
- Implement connection pooling
- Add database indexes
- Optimize AI prompts for token usage

#### 4. Error Handling & Logging
- Implement comprehensive error handling
- Add structured logging
- Set up Sentry for error tracking

**Deliverables:**
- [ ] Unit test coverage > 80%
- [ ] Integration tests for critical paths
- [ ] Performance benchmarks met
- [ ] Error handling and logging complete

---

## Phase 7: Deployment & Monitoring
**Duration:** Week 8-9 (3-5 days)
**Priority:** High

### Tasks

#### 1. Docker Production Build
```dockerfile
# Dockerfile
FROM python:3.11-slim

WORKDIR /app

# Install dependencies
COPY pyproject.toml poetry.lock ./
RUN pip install poetry && \
    poetry config virtualenvs.create false && \
    poetry install --no-dev

# Copy application
COPY . .

# Run migrations and start server
CMD ["sh", "-c", "alembic upgrade head && uvicorn app.main:app --host 0.0.0.0 --port 8000"]
```

#### 2. CI/CD Pipeline
Create `.github/workflows/deploy.yml`:
```yaml
name: Deploy Backend

on:
  push:
    branches: [main]

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3

      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.11'

      - name: Install dependencies
        run: |
          pip install poetry
          poetry install

      - name: Run tests
        run: poetry run pytest

      - name: Deploy to Railway
        uses: bervProject/railway-deploy@main
        with:
          railway_token: ${{ secrets.RAILWAY_TOKEN }}
          service: api
```

#### 3. Monitoring Setup
- Configure Sentry for error tracking
- Set up logging aggregation
- Create health check endpoints
- Monitor API performance

#### 4. Documentation
- API documentation (auto-generated by FastAPI)
- Deployment guide
- Environment variables documentation

**Deliverables:**
- [ ] Docker image built and tested
- [ ] CI/CD pipeline working
- [ ] Deployed to Railway/Fly.io
- [ ] Monitoring and alerting configured
- [ ] Documentation complete

---

## Testing Checklist

### Unit Tests
- [ ] AI generation services
- [ ] Scraping services
- [ ] Authentication utilities
- [ ] Database models

### Integration Tests
- [ ] Full CV generation flow
- [ ] Job scraping and storage
- [ ] Application creation
- [ ] API authentication

### Performance Tests
- [ ] CV generation < 5s
- [ ] Job list query < 500ms
- [ ] API response time < 200ms

### Security Tests
- [ ] JWT token validation
- [ ] SQL injection prevention
- [ ] Rate limiting
- [ ] Input validation

---

## Deployment Checklist

### Pre-Deployment
- [ ] All tests passing
- [ ] Environment variables configured
- [ ] Database migrations ready
- [ ] Secrets stored securely

### Deployment
- [ ] Deploy to staging
- [ ] Run smoke tests
- [ ] Deploy to production
- [ ] Verify health checks

### Post-Deployment
- [ ] Monitor error rates
- [ ] Check API performance
- [ ] Verify background jobs running
- [ ] Test critical user flows

---

## Timeline Summary

| Phase | Duration | Priority | Deliverables |
|-------|----------|----------|--------------|
| 0: Setup | 5-7 days | Critical | Project structure, Docker, FastAPI app |
| 1: Database & Auth | 5-7 days | Critical | Models, migrations, authentication |
| 2: Profile & Projects | 5-7 days | High | Profile/projects CRUD APIs |
| 3: AI Integration | 10-12 days | Critical | CV/cover letter generation |
| 4: Job Scraping | 10-12 days | High | Scraping system, Celery tasks |
| 5: Applications | 5-7 days | Medium | Application management APIs |
| 6: Testing | 5-7 days | High | Unit/integration tests, optimization |
| 7: Deployment | 3-5 days | High | CI/CD, monitoring, production deploy |

**Total:** 8-10 weeks for MVP

---

## Risk Mitigation

| Risk | Mitigation Strategy |
|------|---------------------|
| Job scraping blocked | Multiple sources, API fallbacks, proxy rotation |
| AI API outage | Provider fallback (OpenAI → Anthropic) |
| Rate limits exceeded | Caching layer, request queuing |
| Database performance | Indexing, connection pooling, read replicas |
| High AI costs | Token optimization, caching identical requests |

---

## Success Metrics

- [ ] API uptime: 99%+
- [ ] CV generation: < 5 seconds
- [ ] Job scraping: 50+ jobs/search
- [ ] Test coverage: > 80%
- [ ] Error rate: < 1%

---

**Next Steps:**
1. Review and approve this plan
2. Set up development environment (Phase 0)
3. Begin Phase 1: Database & Authentication
4. Weekly progress reviews

**Note:** Adjust timeline based on your availability and team size. This plan assumes 1 backend developer working full-time.
