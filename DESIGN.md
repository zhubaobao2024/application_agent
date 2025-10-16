# AI Job Application Assistant - System Design Document

**Version:** 1.0
**Last Updated:** 2025-10-15
**Status:** Design Phase

> **Note:** This is a comprehensive system design document. Use the Table of Contents to navigate to specific sections.

---

## Table of Contents
1. [Overview](#overview)
2. [System Architecture](#system-architecture)
3. [Technology Stack](#technology-stack)
4. [Database Schema](#database-schema)
5. [API Design](#api-design)
6. [Component Architecture](#component-architecture)
7. [AI Integration](#ai-integration)
8. [Job Scraping Strategy](#job-scraping-strategy)
9. [Security & Privacy](#security--privacy)
10. [Deployment Architecture](#deployment-architecture)
11. [Development Workflow](#development-workflow)
12. [Scalability Considerations](#scalability-considerations)

---

## Overview

### Product Vision
An AI-powered application that automates the job application process by:
- Collecting relevant job openings from multiple sources
- Adapting user CVs based on job requirements and past projects
- Generating personalized cover letters

### Core Features
1. **Job Discovery Engine**: Automated collection and filtering of job postings
2. **CV Adapter**: AI-powered CV customization for each job
3. **Cover Letter Generator**: Personalized cover letter creation
4. **Application Tracker**: Dashboard to manage application status

### Success Metrics
- CV generation time: < 30 seconds
- Job relevance accuracy: > 85%
- User satisfaction with generated content: > 90%
- System uptime: 99%+

---

## System Architecture

### High-Level Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                         Client Layer                         │
│  ┌────────────────────────────────────────────────────────┐ │
│  │         Next.js 14 Frontend (React + TypeScript)       │ │
│  │  - Server Components - Client Components - UI Library │ │
│  └────────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────┘
                              │
                              │ HTTPS / REST
                              │
┌─────────────────────────────┼─────────────────────────────────┐
│                    Application Layer                          │
│  ┌──────────────────────────┴──────────────────────────────┐ │
│  │           Next.js API Routes (TypeScript)               │ │
│  │  - User Management   - Application CRUD                 │ │
│  │  - Authentication    - Data Aggregation                 │ │
│  └──────────────────────────┬──────────────────────────────┘ │
│                             │                                 │
│  ┌──────────────────────────┴──────────────────────────────┐ │
│  │           FastAPI Service (Python)                      │ │
│  │  - AI Processing     - Job Scraping                     │ │
│  │  - CV Generation     - Document Parsing                 │ │
│  └──────────────────────────┬──────────────────────────────┘ │
└─────────────────────────────┼─────────────────────────────────┘
                              │
         ┌────────────────────┼────────────────────┐
         │                    │                    │
         ▼                    ▼                    ▼
┌─────────────────┐  ┌─────────────────┐  ┌──────────────────┐
│  Supabase       │  │  OpenAI API     │  │  Job Board APIs  │
│  (PostgreSQL +  │  │  Anthropic API  │  │  - LinkedIn      │
│   Auth)         │  │                 │  │  - Indeed        │
└─────────────────┘  └─────────────────┘  │  - Greenhouse    │
                                           └──────────────────┘
```

### Architecture Principles

1. **Separation of Concerns**: Frontend (Next.js) handles UI/UX, Python service handles AI/ML
2. **API-First Design**: All services communicate via well-defined REST APIs
3. **Microservices-Ready**: Core services can be scaled independently
4. **Stateless Services**: All state stored in database, services are stateless
5. **Async Processing**: Long-running tasks (scraping, AI generation) use job queues

---

## Technology Stack

### Frontend Stack

| Technology | Purpose | Justification |
|------------|---------|---------------|
| **Next.js 14** | React Framework | - SSR/SSG for better SEO<br>- App Router for modern routing<br>- Built-in API routes<br>- Excellent developer experience |
| **TypeScript** | Type Safety | - Catch errors at compile time<br>- Better IDE support<br>- Self-documenting code |
| **Tailwind CSS** | Styling | - Utility-first CSS<br>- Fast prototyping<br>- Consistent design system |
| **shadcn/ui** | UI Components | - Accessible components<br>- Customizable<br>- Built on Radix UI |
| **TanStack Query** | Data Fetching | - Caching & synchronization<br>- Optimistic updates<br>- Background refetching |
| **Zustand** | State Management | - Lightweight (< 1KB)<br>- Simple API<br>- No boilerplate |
| **React Hook Form** | Forms | - Performance (uncontrolled)<br>- Easy validation with Zod<br>- Great UX |
| **Zod** | Schema Validation | - TypeScript-first<br>- Runtime validation<br>- Type inference |

### Backend Stack

| Technology | Purpose | Justification |
|------------|---------|---------------|
| **FastAPI** | Python Framework | - Async support<br>- Auto-generated docs<br>- Pydantic validation<br>- Fast performance |
| **Poetry** | Dependency Management | - Deterministic builds<br>- Lock files<br>- Virtual env management |
| **SQLAlchemy** | ORM | - Powerful query builder<br>- Migration support<br>- Type hints |
| **Celery** | Task Queue | - Async job processing<br>- Retry logic<br>- Scheduled tasks |
| **Redis** | Cache & Queue | - Job queue backend<br>- Rate limiting<br>- Session storage |

### AI & ML Stack

| Technology | Purpose | Justification |
|------------|---------|---------------|
| **OpenAI GPT-4o** | Text Generation | - Best-in-class quality<br>- Fast API responses<br>- Structured outputs |
| **Anthropic Claude** | Document Analysis | - Long context window<br>- Better reasoning<br>- Backup provider |
| **LangChain** | AI Orchestration | - Prompt management<br>- Chain complex operations<br>- Provider abstraction |
| **tiktoken** | Token Counting | - Accurate cost estimation<br>- Optimize prompts |

### Data & Infrastructure

| Technology | Purpose | Justification |
|------------|---------|---------------|
| **PostgreSQL** | Primary Database | - ACID compliance<br>- JSON support<br>- Full-text search |
| **Supabase** | Backend-as-a-Service | - Managed PostgreSQL<br>- Built-in auth<br>- Real-time subscriptions<br>- Free tier |
| **Vercel** | Frontend Hosting | - Zero-config Next.js<br>- Edge functions<br>- Automatic HTTPS |
| **Railway/Fly.io** | Backend Hosting | - Easy Docker deployment<br>- Auto-scaling<br>- Generous free tier |
| **Docker** | Containerization | - Consistent environments<br>- Easy local development |

### Development Tools

| Technology | Purpose |
|------------|---------|
| **pnpm** | Package manager (faster than npm) |
| **Turborepo** | Monorepo build system |
| **ESLint** | Code linting |
| **Prettier** | Code formatting |
| **Husky** | Git hooks |
| **Vitest** | Frontend testing |
| **pytest** | Backend testing |
| **Playwright** | E2E testing & web scraping |

---

## Database Schema

### Entity Relationship Diagram

```
┌─────────────┐         ┌──────────────┐         ┌─────────────┐
│   users     │────┬───│ user_profiles│         │   projects  │
│  (Supabase) │    │    └──────────────┘         └─────────────┘
└─────────────┘    │            │                       │
                   │            └───────────────────────┤
                   │                                    │
                   │                                    │
                   ├────────────────────┐               │
                   │                    │               │
                   ▼                    ▼               ▼
         ┌──────────────────┐  ┌──────────────┐  ┌──────────────┐
         │   applications   │──│     jobs     │  │  cv_templates│
         └──────────────────┘  └──────────────┘  └──────────────┘
                   │                    │
                   ├────────────────────┤
                   │                    │
                   ▼                    ▼
         ┌──────────────────┐  ┌──────────────────┐
         │  generated_cvs   │  │ cover_letters    │
         └──────────────────┘  └──────────────────┘
```

### Schema Definitions

#### `users` (Managed by Supabase Auth)
```sql
-- Managed by Supabase, contains:
-- id, email, encrypted_password, email_confirmed_at, etc.
```

#### `user_profiles`
```sql
CREATE TABLE user_profiles (
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  user_id UUID REFERENCES auth.users(id) ON DELETE CASCADE,
  full_name VARCHAR(255) NOT NULL,
  phone VARCHAR(50),
  location VARCHAR(255),
  linkedin_url VARCHAR(500),
  github_url VARCHAR(500),
  portfolio_url VARCHAR(500),

  -- Preferences
  target_roles TEXT[], -- ["Software Engineer", "ML Engineer"]
  preferred_locations TEXT[], -- ["Remote", "San Francisco"]
  desired_salary_min INTEGER,
  desired_salary_max INTEGER,
  willing_to_relocate BOOLEAN DEFAULT false,

  -- Base CV content
  summary TEXT,
  skills JSONB, -- {"technical": ["Python", "React"], "soft": [...]}
  education JSONB, -- Array of education entries
  work_experience JSONB, -- Array of work experience entries

  created_at TIMESTAMPTZ DEFAULT NOW(),
  updated_at TIMESTAMPTZ DEFAULT NOW(),

  UNIQUE(user_id)
);

CREATE INDEX idx_user_profiles_user_id ON user_profiles(user_id);
```

#### `projects`
```sql
CREATE TABLE projects (
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  user_id UUID REFERENCES auth.users(id) ON DELETE CASCADE,

  title VARCHAR(255) NOT NULL,
  description TEXT,
  detailed_description TEXT, -- For AI context
  technologies TEXT[], -- ["React", "Node.js", "PostgreSQL"]

  role VARCHAR(100), -- "Lead Developer", "Solo Developer"
  start_date DATE,
  end_date DATE, -- NULL if ongoing

  github_url VARCHAR(500),
  demo_url VARCHAR(500),

  achievements TEXT[], -- Bullet points of key achievements
  metrics JSONB, -- {"users": 10000, "performance_improvement": "40%"}

  is_featured BOOLEAN DEFAULT false, -- Show on all CVs
  relevance_tags TEXT[], -- ["web", "backend", "ml"] for matching

  created_at TIMESTAMPTZ DEFAULT NOW(),
  updated_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE INDEX idx_projects_user_id ON projects(user_id);
CREATE INDEX idx_projects_tags ON projects USING GIN(relevance_tags);
```

#### `jobs`
```sql
CREATE TABLE jobs (
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),

  -- Source information
  external_id VARCHAR(255), -- ID from source platform
  source VARCHAR(50) NOT NULL, -- "linkedin", "indeed", "greenhouse"
  source_url VARCHAR(1000) NOT NULL,

  -- Job details
  title VARCHAR(255) NOT NULL,
  company VARCHAR(255) NOT NULL,
  company_logo_url VARCHAR(500),
  location VARCHAR(255),
  remote_type VARCHAR(50), -- "remote", "hybrid", "onsite"

  description TEXT NOT NULL,
  requirements TEXT,
  responsibilities TEXT,

  -- Structured data
  salary_min INTEGER,
  salary_max INTEGER,
  salary_currency VARCHAR(10) DEFAULT 'USD',
  employment_type VARCHAR(50), -- "full-time", "contract", "internship"
  experience_level VARCHAR(50), -- "entry", "mid", "senior", "lead"

  required_skills TEXT[],
  preferred_skills TEXT[],
  benefits TEXT[],

  -- Metadata
  posted_date TIMESTAMPTZ,
  scraped_at TIMESTAMPTZ DEFAULT NOW(),
  expires_at TIMESTAMPTZ,
  is_active BOOLEAN DEFAULT true,

  -- AI-generated fields
  parsed_requirements JSONB, -- Structured extraction of requirements
  relevance_score FLOAT, -- Match score with user profile

  created_at TIMESTAMPTZ DEFAULT NOW(),
  updated_at TIMESTAMPTZ DEFAULT NOW(),

  UNIQUE(external_id, source)
);

CREATE INDEX idx_jobs_source ON jobs(source);
CREATE INDEX idx_jobs_active ON jobs(is_active) WHERE is_active = true;
CREATE INDEX idx_jobs_posted_date ON jobs(posted_date DESC);
CREATE INDEX idx_jobs_skills ON jobs USING GIN(required_skills);
CREATE INDEX idx_jobs_title_company ON jobs(title, company);

-- Full-text search
CREATE INDEX idx_jobs_fts ON jobs USING GIN(
  to_tsvector('english', title || ' ' || company || ' ' || description)
);
```

#### `applications`
```sql
CREATE TABLE applications (
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  user_id UUID REFERENCES auth.users(id) ON DELETE CASCADE,
  job_id UUID REFERENCES jobs(id) ON DELETE CASCADE,

  -- Status tracking
  status VARCHAR(50) DEFAULT 'draft', -- draft, applied, interviewing, offered, rejected, accepted
  applied_at TIMESTAMPTZ,

  -- Application materials
  cv_id UUID REFERENCES generated_cvs(id),
  cover_letter_id UUID REFERENCES cover_letters(id),

  -- Notes & tracking
  notes TEXT,
  follow_up_date DATE,
  interview_dates JSONB, -- Array of interview schedule

  -- External tracking
  external_application_id VARCHAR(255), -- If applied through API
  source_applied VARCHAR(50), -- "linkedin", "direct", "email"

  created_at TIMESTAMPTZ DEFAULT NOW(),
  updated_at TIMESTAMPTZ DEFAULT NOW(),

  UNIQUE(user_id, job_id)
);

CREATE INDEX idx_applications_user_id ON applications(user_id);
CREATE INDEX idx_applications_job_id ON applications(job_id);
CREATE INDEX idx_applications_status ON applications(status);
```

#### `generated_cvs`
```sql
CREATE TABLE generated_cvs (
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  user_id UUID REFERENCES auth.users(id) ON DELETE CASCADE,
  job_id UUID REFERENCES jobs(id) ON DELETE SET NULL,

  -- Content
  content JSONB NOT NULL, -- Structured CV content
  html_content TEXT, -- Rendered HTML
  pdf_url VARCHAR(500), -- S3/Storage URL

  -- Generation metadata
  template_id UUID REFERENCES cv_templates(id),
  ai_model VARCHAR(50), -- "gpt-4o", "claude-3.5-sonnet"
  generation_params JSONB, -- Prompt settings, temperature, etc.

  -- Selected content
  included_projects UUID[], -- Which projects were included
  highlighted_skills TEXT[], -- Which skills were emphasized

  -- Versioning
  version INTEGER DEFAULT 1,
  is_latest BOOLEAN DEFAULT true,

  created_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE INDEX idx_generated_cvs_user_id ON generated_cvs(user_id);
CREATE INDEX idx_generated_cvs_job_id ON generated_cvs(job_id);
```

#### `cover_letters`
```sql
CREATE TABLE cover_letters (
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  user_id UUID REFERENCES auth.users(id) ON DELETE CASCADE,
  job_id UUID REFERENCES jobs(id) ON DELETE SET NULL,

  content TEXT NOT NULL,
  tone VARCHAR(50) DEFAULT 'professional', -- professional, enthusiastic, casual

  -- Generation metadata
  ai_model VARCHAR(50),
  generation_params JSONB,

  created_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE INDEX idx_cover_letters_user_id ON cover_letters(user_id);
CREATE INDEX idx_cover_letters_job_id ON cover_letters(job_id);
```

#### `cv_templates`
```sql
CREATE TABLE cv_templates (
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  name VARCHAR(100) NOT NULL,
  description TEXT,

  -- Template configuration
  layout_config JSONB, -- Colors, fonts, spacing
  sections_order TEXT[], -- ["summary", "experience", "projects", "skills"]

  -- Preview
  thumbnail_url VARCHAR(500),

  is_default BOOLEAN DEFAULT false,
  is_public BOOLEAN DEFAULT true, -- User-created vs system templates
  created_by UUID REFERENCES auth.users(id),

  created_at TIMESTAMPTZ DEFAULT NOW()
);
```

#### `user_job_preferences`
```sql
CREATE TABLE user_job_preferences (
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  user_id UUID REFERENCES auth.users(id) ON DELETE CASCADE,
  job_id UUID REFERENCES jobs(id) ON DELETE CASCADE,

  is_favorited BOOLEAN DEFAULT false,
  is_hidden BOOLEAN DEFAULT false,
  custom_notes TEXT,

  created_at TIMESTAMPTZ DEFAULT NOW(),
  updated_at TIMESTAMPTZ DEFAULT NOW(),

  UNIQUE(user_id, job_id)
);
```

### Row Level Security (RLS) Policies

```sql
-- Example RLS for user_profiles
ALTER TABLE user_profiles ENABLE ROW LEVEL SECURITY;

CREATE POLICY "Users can view own profile"
  ON user_profiles FOR SELECT
  USING (auth.uid() = user_id);

CREATE POLICY "Users can update own profile"
  ON user_profiles FOR UPDATE
  USING (auth.uid() = user_id);

-- Similar policies for projects, applications, generated_cvs, cover_letters
```

---

## API Design

### Next.js API Routes (TypeScript)

#### Authentication
```typescript
// /api/auth/signup
POST /api/auth/signup
Request: { email: string, password: string, fullName: string }
Response: { user: User, session: Session }

// /api/auth/login
POST /api/auth/login
Request: { email: string, password: string }
Response: { user: User, session: Session }

// /api/auth/logout
POST /api/auth/logout
Response: { success: boolean }
```

#### User Profile
```typescript
// /api/profile
GET /api/profile
Response: { profile: UserProfile, projects: Project[] }

PUT /api/profile
Request: { profile: Partial<UserProfile> }
Response: { profile: UserProfile }

// /api/profile/projects
POST /api/profile/projects
Request: { project: Project }
Response: { project: Project }

PUT /api/profile/projects/:id
Request: { project: Partial<Project> }
Response: { project: Project }

DELETE /api/profile/projects/:id
Response: { success: boolean }
```

#### Jobs
```typescript
// /api/jobs
GET /api/jobs?page=1&limit=20&source=linkedin&remote=true
Response: {
  jobs: Job[],
  pagination: { page, limit, total, hasMore }
}

GET /api/jobs/:id
Response: { job: Job }

// /api/jobs/search
POST /api/jobs/search
Request: {
  query: string,
  filters: { locations, skills, experience_level, salary_min }
}
Response: { jobs: Job[], total: number }

// /api/jobs/:id/favorite
POST /api/jobs/:id/favorite
Response: { success: boolean }
```

#### Applications
```typescript
// /api/applications
GET /api/applications?status=applied
Response: { applications: Application[] }

POST /api/applications
Request: {
  jobId: string,
  cvId?: string,
  coverLetterId?: string,
  notes?: string
}
Response: { application: Application }

PUT /api/applications/:id
Request: { status: string, notes: string }
Response: { application: Application }
```

### FastAPI Routes (Python)

#### AI Generation
```python
# /api/ai/cv/generate
POST /api/ai/cv/generate
Request: {
  "user_id": "uuid",
  "job_id": "uuid",
  "template_id": "uuid",
  "options": {
    "tone": "professional",
    "emphasize_skills": ["Python", "React"],
    "include_projects": ["uuid1", "uuid2"]
  }
}
Response: {
  "cv_id": "uuid",
  "content": {...},
  "pdf_url": "https://...",
  "generation_time_ms": 2300
}

# /api/ai/cover-letter/generate
POST /api/ai/cover-letter/generate
Request: {
  "user_id": "uuid",
  "job_id": "uuid",
  "tone": "enthusiastic",
  "key_points": ["5 years Python", "Led team of 3"]
}
Response: {
  "cover_letter_id": "uuid",
  "content": "Dear Hiring Manager...",
  "generation_time_ms": 1800
}

# /api/ai/cv/analyze
POST /api/ai/cv/analyze
Request: {
  "cv_content": "...",
  "job_description": "..."
}
Response: {
  "match_score": 0.85,
  "missing_keywords": ["Docker", "Kubernetes"],
  "suggestions": ["Add more metrics to achievements"]
}
```

#### Job Scraping
```python
# /api/scraper/trigger
POST /api/scraper/trigger
Request: {
  "user_id": "uuid",
  "sources": ["linkedin", "indeed"],
  "preferences": {
    "roles": ["Software Engineer"],
    "locations": ["Remote"],
    "experience_level": ["mid", "senior"]
  }
}
Response: {
  "job_id": "celery_task_id",
  "status": "queued"
}

# /api/scraper/status/:job_id
GET /api/scraper/status/:job_id
Response: {
  "status": "completed",
  "jobs_found": 47,
  "jobs_saved": 35
}
```

#### Document Parsing
```python
# /api/parser/cv
POST /api/parser/cv
Request: multipart/form-data (PDF or DOCX file)
Response: {
  "parsed_content": {
    "name": "John Doe",
    "email": "john@example.com",
    "experience": [...],
    "skills": [...],
    "education": [...]
  },
  "confidence_score": 0.92
}
```

### API Authentication

```typescript
// All API calls include JWT token from Supabase
headers: {
  'Authorization': 'Bearer <supabase_jwt_token>',
  'Content-Type': 'application/json'
}
```

### API Error Handling

```typescript
// Standardized error response
{
  "error": {
    "code": "INVALID_INPUT",
    "message": "Job ID is required",
    "details": { "field": "job_id" }
  },
  "timestamp": "2025-10-15T10:30:00Z",
  "request_id": "req_abc123"
}
```

---

## Component Architecture

### Frontend Component Hierarchy

```
app/
├── (auth)/
│   ├── login/
│   │   └── page.tsx              # Login page
│   ├── signup/
│   │   └── page.tsx              # Signup page
│   └── layout.tsx                # Auth layout (centered form)
│
├── (dashboard)/
│   ├── layout.tsx                # Dashboard layout (sidebar + header)
│   ├── page.tsx                  # Dashboard home
│   │
│   ├── jobs/
│   │   ├── page.tsx              # Job list view
│   │   ├── [id]/
│   │   │   └── page.tsx          # Job detail view
│   │   └── components/
│   │       ├── JobCard.tsx
│   │       ├── JobFilters.tsx
│   │       └── JobSearch.tsx
│   │
│   ├── applications/
│   │   ├── page.tsx              # Application tracker
│   │   ├── [id]/
│   │   │   └── page.tsx          # Application detail
│   │   └── components/
│   │       ├── ApplicationCard.tsx
│   │       ├── StatusPipeline.tsx
│   │       └── TimelineView.tsx
│   │
│   ├── profile/
│   │   ├── page.tsx              # Profile overview
│   │   ├── edit/
│   │   │   └── page.tsx          # Edit profile
│   │   ├── projects/
│   │   │   ├── page.tsx          # Manage projects
│   │   │   └── [id]/
│   │   │       └── page.tsx      # Edit project
│   │   └── components/
│   │       ├── ProfileForm.tsx
│   │       ├── ProjectForm.tsx
│   │       └── SkillsManager.tsx
│   │
│   └── generate/
│       ├── page.tsx              # Generation wizard
│       └── components/
│           ├── CVPreview.tsx
│           ├── CoverLetterEditor.tsx
│           └── TemplateSelector.tsx
│
├── api/
│   ├── auth/
│   ├── profile/
│   ├── jobs/
│   └── applications/
│
└── components/
    ├── ui/                       # shadcn/ui components
    │   ├── button.tsx
    │   ├── card.tsx
    │   ├── input.tsx
    │   └── ...
    ├── layout/
    │   ├── Header.tsx
    │   ├── Sidebar.tsx
    │   └── Footer.tsx
    └── shared/
        ├── LoadingSpinner.tsx
        ├── ErrorBoundary.tsx
        └── EmptyState.tsx
```

### Key React Components

```typescript
// JobCard.tsx
interface JobCardProps {
  job: Job;
  onApply: (jobId: string) => void;
  onFavorite: (jobId: string) => void;
  showMatchScore?: boolean;
}

// CVPreview.tsx
interface CVPreviewProps {
  cvContent: CVContent;
  template: CVTemplate;
  onEdit: () => void;
  onDownload: () => void;
}

// ApplicationCard.tsx
interface ApplicationCardProps {
  application: Application;
  onStatusChange: (status: ApplicationStatus) => void;
  onAddNote: (note: string) => void;
}
```

### State Management Strategy

```typescript
// Global state (Zustand)
interface AppState {
  user: User | null;
  profile: UserProfile | null;
  setUser: (user: User) => void;
  setProfile: (profile: UserProfile) => void;
}

// Server state (TanStack Query)
const { data: jobs } = useQuery({
  queryKey: ['jobs', filters],
  queryFn: () => fetchJobs(filters),
  staleTime: 5 * 60 * 1000, // 5 minutes
});

const { mutate: generateCV } = useMutation({
  mutationFn: generateCVForJob,
  onSuccess: () => {
    queryClient.invalidateQueries(['cvs']);
  },
});
```

---

## AI Integration

### Prompt Engineering Strategy

#### CV Generation Prompt Template
```python
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
```

#### Cover Letter Prompt Template
```python
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
```

### AI Provider Abstraction

```python
# ai/providers.py
class AIProvider(ABC):
    @abstractmethod
    async def generate_completion(
        self,
        prompt: str,
        **kwargs
    ) -> str:
        pass

class OpenAIProvider(AIProvider):
    async def generate_completion(self, prompt: str, **kwargs):
        response = await openai.ChatCompletion.acreate(
            model="gpt-4o",
            messages=[{"role": "user", "content": prompt}],
            **kwargs
        )
        return response.choices[0].message.content

class AnthropicProvider(AIProvider):
    async def generate_completion(self, prompt: str, **kwargs):
        response = await anthropic.messages.create(
            model="claude-3-5-sonnet-20241022",
            messages=[{"role": "user", "content": prompt}],
            **kwargs
        )
        return response.content[0].text

# Factory pattern for failover
async def generate_with_fallback(prompt: str):
    try:
        return await OpenAIProvider().generate_completion(prompt)
    except Exception as e:
        logger.warning(f"OpenAI failed: {e}, trying Anthropic")
        return await AnthropicProvider().generate_completion(prompt)
```

### Token Optimization

```python
# Estimate cost before generation
def estimate_generation_cost(
    user_profile: dict,
    job_description: str
) -> float:
    prompt = build_cv_prompt(user_profile, job_description)
    token_count = tiktoken.encode(prompt)

    # GPT-4o pricing: $2.50 / 1M input, $10 / 1M output
    input_cost = (token_count / 1_000_000) * 2.50
    estimated_output_tokens = 1500
    output_cost = (estimated_output_tokens / 1_000_000) * 10

    return input_cost + output_cost

# Cache frequently used prompts
@lru_cache(maxsize=100)
def get_base_prompt_template(template_type: str) -> str:
    return PROMPT_TEMPLATES[template_type]
```

---

## Job Scraping Strategy

### Scraping Architecture

```
┌─────────────────────────────────────────────────────┐
│              Celery Beat (Scheduler)                │
│  - Daily scraping tasks                             │
│  - User-specific scheduled searches                 │
└─────────────────┬───────────────────────────────────┘
                  │
                  ▼
┌─────────────────────────────────────────────────────┐
│            Celery Workers (Task Queue)              │
│  - Process scraping jobs                            │
│  - Retry on failure                                 │
│  - Rate limiting                                    │
└─────────────────┬───────────────────────────────────┘
                  │
        ┌─────────┴─────────┬─────────────┐
        │                   │             │
        ▼                   ▼             ▼
┌──────────────┐   ┌──────────────┐  ┌──────────────┐
│  LinkedIn    │   │   Indeed     │  │  Greenhouse  │
│  Scraper     │   │   Scraper    │  │   API        │
└──────────────┘   └──────────────┘  └──────────────┘
```

### Scraping Methods by Source

| Source | Method | Rate Limit | Notes |
|--------|--------|------------|-------|
| **LinkedIn** | Playwright (headless browser) | 50 req/hour | Requires login, high detection risk |
| **Indeed** | API + Web scraping | 100 req/hour | Public API available for partners |
| **Greenhouse** | Public API | 1000 req/day | Best option, structured data |
| **AngelList** | Web scraping | 30 req/hour | Startups focus |
| **RemoteOK** | RSS feed | Unlimited | Easy to parse |

### Scraper Implementation

```python
# scrapers/base.py
class JobScraper(ABC):
    def __init__(self):
        self.rate_limiter = RateLimiter()

    @abstractmethod
    async def scrape_jobs(
        self,
        search_params: SearchParams
    ) -> List[RawJob]:
        pass

    async def parse_job(self, raw_html: str) -> Job:
        """Use AI to extract structured data from HTML"""
        prompt = f"Extract job details from:\n{raw_html}"
        result = await ai_provider.generate_completion(prompt)
        return Job(**json.loads(result))

# scrapers/linkedin.py
class LinkedInScraper(JobScraper):
    async def scrape_jobs(self, params: SearchParams):
        async with async_playwright() as p:
            browser = await p.chromium.launch(headless=True)
            page = await browser.new_page()

            # Login
            await page.goto("https://linkedin.com/login")
            await page.fill("#username", os.getenv("LINKEDIN_EMAIL"))
            await page.fill("#password", os.getenv("LINKEDIN_PASSWORD"))
            await page.click("[type=submit]")

            # Search
            search_url = self.build_search_url(params)
            await page.goto(search_url)

            # Extract job cards
            jobs = await page.query_selector_all(".job-card")

            results = []
            for job_element in jobs:
                await self.rate_limiter.wait()
                job_data = await self.extract_job_data(job_element)
                results.append(job_data)

            await browser.close()
            return results
```

### Deduplication Strategy

```python
def deduplicate_job(job: RawJob) -> bool:
    """Check if job already exists in database"""

    # Exact match on external_id + source
    if Job.query.filter_by(
        external_id=job.external_id,
        source=job.source
    ).first():
        return True

    # Fuzzy match on title + company (account for reposts)
    similar = Job.query.filter(
        Job.title.ilike(f"%{job.title}%"),
        Job.company.ilike(f"%{job.company}%"),
        Job.posted_date > datetime.now() - timedelta(days=30)
    ).first()

    if similar:
        # Check similarity score
        similarity = fuzz.ratio(
            job.description,
            similar.description
        )
        return similarity > 0.85

    return False
```

### Anti-Bot Detection Measures

```python
# Random delays
await asyncio.sleep(random.uniform(2, 5))

# Rotate user agents
user_agents = [...]
random_ua = random.choice(user_agents)

# Use residential proxies for production
proxies = ProxyRotator(provider="brightdata")

# Human-like behavior
await page.mouse.move(
    random.randint(100, 500),
    random.randint(100, 500)
)
```

---

## Security & Privacy

### Data Protection

1. **Encryption at Rest**
   - All sensitive data encrypted in PostgreSQL using pgcrypto
   - Environment variables stored in secure vaults (Vercel/Railway secrets)

2. **Encryption in Transit**
   - HTTPS only (enforced by Vercel/Railway)
   - TLS 1.3 for all API communications

3. **Authentication & Authorization**
   - JWT tokens from Supabase (auto-refresh)
   - Row Level Security (RLS) on all tables
   - API key rotation every 90 days

4. **API Security**
   ```python
   # Rate limiting
   @limiter.limit("10/minute")
   async def generate_cv(request: Request):
       ...

   # Input validation
   class CVGenerationRequest(BaseModel):
       user_id: UUID
       job_id: UUID

       @validator('user_id')
       def validate_user_id(cls, v, values, **kwargs):
           # Ensure user_id matches authenticated user
           if v != request.state.user.id:
               raise ValueError("Unauthorized")
           return v
   ```

5. **Data Retention**
   - Personal data deleted within 30 days of account deletion
   - Generated CVs retained for 90 days
   - Job data refreshed every 7 days (old jobs archived)

### GDPR Compliance

```python
# User data export
async def export_user_data(user_id: UUID) -> dict:
    """Export all user data in JSON format"""
    return {
        "profile": user_profile,
        "projects": user_projects,
        "applications": user_applications,
        "generated_cvs": user_cvs,
        "cover_letters": user_cover_letters,
    }

# Right to be forgotten
async def delete_user_account(user_id: UUID):
    """Permanently delete all user data"""
    async with db.transaction():
        await db.execute("DELETE FROM user_profiles WHERE user_id = $1", user_id)
        await db.execute("DELETE FROM projects WHERE user_id = $1", user_id)
        # ... delete all related data
        await auth.delete_user(user_id)
```

### Secrets Management

```bash
# .env.example
DATABASE_URL=
SUPABASE_URL=
SUPABASE_ANON_KEY=
SUPABASE_SERVICE_KEY=

OPENAI_API_KEY=
ANTHROPIC_API_KEY=

REDIS_URL=

# Job board credentials
LINKEDIN_EMAIL=
LINKEDIN_PASSWORD=
INDEED_API_KEY=

# Production only
SENTRY_DSN=
POSTHOG_API_KEY=
```

---

## Deployment Architecture

### Production Infrastructure

```
                        ┌─────────────────┐
                        │   Cloudflare    │
                        │   (CDN + DDoS)  │
                        └────────┬────────┘
                                 │
                    ┌────────────┴────────────┐
                    │                         │
            ┌───────▼────────┐       ┌───────▼────────┐
            │  Vercel         │       │  Railway/Fly   │
            │  (Next.js)      │       │  (FastAPI)     │
            │  - Edge Runtime │       │  - Docker      │
            │  - Auto-scale   │       │  - Auto-scale  │
            └───────┬─────────┘       └───────┬────────┘
                    │                         │
                    └────────────┬────────────┘
                                 │
                    ┌────────────┴────────────┐
                    │                         │
            ┌───────▼────────┐       ┌───────▼────────┐
            │   Supabase     │       │    Redis       │
            │  (PostgreSQL)  │       │  (Upstash)     │
            │  - Auto-backup │       │  - Managed     │
            └────────────────┘       └────────────────┘
```

### Deployment Environments

| Environment | Purpose | URL | Auto-deploy |
|-------------|---------|-----|-------------|
| **Development** | Local dev | localhost | Manual |
| **Preview** | PR previews | pr-123.vercel.app | On PR |
| **Staging** | Pre-production | staging.app.com | On merge to develop |
| **Production** | Live app | app.com | On merge to main |

### CI/CD Pipeline

```yaml
# .github/workflows/ci.yml
name: CI/CD

on:
  push:
    branches: [main, develop]
  pull_request:

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - uses: pnpm/action-setup@v2

      - name: Install dependencies
        run: pnpm install

      - name: Lint
        run: pnpm lint

      - name: Type check
        run: pnpm type-check

      - name: Test
        run: pnpm test

      - name: E2E tests
        run: pnpm test:e2e

  deploy-frontend:
    needs: test
    if: github.ref == 'refs/heads/main'
    runs-on: ubuntu-latest
    steps:
      - name: Deploy to Vercel
        uses: amondnet/vercel-action@v20
        with:
          vercel-token: ${{ secrets.VERCEL_TOKEN }}
          vercel-org-id: ${{ secrets.ORG_ID }}
          vercel-project-id: ${{ secrets.PROJECT_ID }}
          vercel-args: '--prod'

  deploy-backend:
    needs: test
    if: github.ref == 'refs/heads/main'
    runs-on: ubuntu-latest
    steps:
      - name: Deploy to Railway
        uses: bervProject/railway-deploy@main
        with:
          railway_token: ${{ secrets.RAILWAY_TOKEN }}
          service: api
```

### Monitoring & Observability

```typescript
// Sentry for error tracking
Sentry.init({
  dsn: process.env.SENTRY_DSN,
  environment: process.env.NODE_ENV,
  tracesSampleRate: 1.0,
});

// PostHog for analytics
posthog.init(process.env.POSTHOG_API_KEY, {
  api_host: 'https://app.posthog.com',
});

// Custom metrics
logger.info('cv_generated', {
  user_id,
  job_id,
  generation_time_ms,
  model: 'gpt-4o',
});
```

---

## Development Workflow

### Local Development Setup

```bash
# 1. Clone repository
git clone <repository-url>
cd application_agent

# 2. Install dependencies
pnpm install
cd apps/api && poetry install

# 3. Set up environment variables
cp .env.example .env
# Fill in your API keys

# 4. Start database
docker-compose up -d postgres redis

# 5. Run migrations
pnpm db:migrate

# 6. Start development servers
pnpm dev          # Frontend on :3000
pnpm dev:api      # Backend on :8000

# 7. Open app
open http://localhost:3000
```

### Git Workflow

```
main (production)
  └── develop (staging)
      ├── feature/job-scraping
      ├── feature/cv-generation
      └── bugfix/auth-issue
```

**Branch naming:**
- `feature/description` - New features
- `bugfix/description` - Bug fixes
- `hotfix/description` - Urgent production fixes
- `refactor/description` - Code refactoring

**Commit conventions:**
```
feat: Add LinkedIn job scraper
fix: Resolve CV generation timeout
docs: Update API documentation
test: Add tests for CV adapter
refactor: Extract prompt templates
```

### Code Review Checklist

- [ ] Code follows TypeScript/Python style guide
- [ ] Tests added/updated and passing
- [ ] No console.log or print statements
- [ ] Error handling implemented
- [ ] Security considerations addressed
- [ ] Performance implications considered
- [ ] Documentation updated

---

## Scalability Considerations

### Performance Targets

| Metric | Target | Strategy |
|--------|--------|----------|
| **CV Generation** | < 5s | Parallel processing, optimized prompts |
| **Job Search** | < 500ms | Database indexing, caching |
| **Page Load** | < 2s | SSR, code splitting, CDN |
| **API Response** | < 200ms | Query optimization, Redis cache |

### Scaling Strategy

#### Phase 1: MVP (0-100 users)
- Single Vercel instance (frontend)
- Single Railway instance (backend)
- Supabase free tier
- No caching needed

#### Phase 2: Growth (100-1000 users)
- Vercel auto-scaling
- Railway scale to 2-3 instances
- Redis caching layer
- CDN for static assets
- Database connection pooling

#### Phase 3: Scale (1000+ users)
- Vercel Edge Functions for global latency
- Railway auto-scaling (5-10 instances)
- Supabase Pro tier (connection pooling)
- Separate read replicas
- Job queue with multiple workers
- AI response caching

### Caching Strategy

```python
# Cache job listings (5 minutes)
@cache(ttl=300)
async def get_jobs(filters: dict):
    return db.query(Job).filter_by(**filters).all()

# Cache AI generations (1 hour for same input)
@cache(ttl=3600)
async def generate_cv(user_id: str, job_id: str):
    # Check if exact same request was made recently
    cache_key = f"cv:{user_id}:{job_id}"
    cached = redis.get(cache_key)
    if cached:
        return json.loads(cached)

    result = await ai_generate(...)
    redis.set(cache_key, json.dumps(result), ex=3600)
    return result
```

### Database Optimization

```sql
-- Partitioning for jobs table (by posted_date)
CREATE TABLE jobs_2024_10 PARTITION OF jobs
FOR VALUES FROM ('2024-10-01') TO ('2024-11-01');

-- Materialized view for job statistics
CREATE MATERIALIZED VIEW job_stats AS
SELECT
  source,
  DATE_TRUNC('day', posted_date) as date,
  COUNT(*) as job_count,
  AVG(salary_min) as avg_salary
FROM jobs
GROUP BY source, DATE_TRUNC('day', posted_date);

-- Refresh daily
REFRESH MATERIALIZED VIEW CONCURRENTLY job_stats;
```

---

## Appendix

### Technology Decision Matrix

| Decision | Options Considered | Chosen | Reason |
|----------|-------------------|---------|--------|
| Frontend Framework | Next.js, Remix, SvelteKit | Next.js 14 | Best ecosystem, SSR, Vercel deployment |
| Backend Language | Node.js, Python, Go | Python | Better AI/ML libraries |
| Database | PostgreSQL, MongoDB, MySQL | PostgreSQL | Structured data, ACID, JSON support |
| AI Provider | OpenAI, Anthropic, Local LLM | OpenAI + Anthropic | Quality + redundancy |
| Hosting | Vercel, AWS, GCP | Vercel + Railway | Easy deployment, free tiers |

### Cost Estimation (Monthly)

#### MVP (100 users)
- Vercel: $0 (hobby tier)
- Railway: $5 (starter)
- Supabase: $0 (free tier)
- OpenAI API: ~$50 (avg 2 generations/user)
- **Total: ~$55/month**

#### Growth (1000 users)
- Vercel: $20 (pro tier)
- Railway: $50 (scaling)
- Supabase: $25 (pro tier)
- OpenAI API: ~$500
- Redis: $10 (Upstash)
- Monitoring: $20 (Sentry + PostHog)
- **Total: ~$625/month**

### Risks & Mitigation

| Risk | Impact | Probability | Mitigation |
|------|--------|-------------|------------|
| Job scraping blocked | High | Medium | Multiple sources, API fallbacks |
| AI API outage | High | Low | Provider fallback, retry logic |
| Rate limit exceeded | Medium | Medium | Caching, batch processing |
| Data breach | Critical | Low | Encryption, security audits |
| Scaling costs | Medium | High | Usage limits, optimize prompts |

### Success Metrics (KPIs)

**Technical:**
- API uptime: 99.5%+
- Average response time: < 500ms
- Error rate: < 1%
- Test coverage: > 80%

**Product:**
- Time to generate application: < 5 minutes
- CV match score: > 80% average
- User retention: > 60% (month 1)
- Applications submitted: 10+ per user per month

**Business:**
- User acquisition cost: < $10
- Monthly active users: 1000+ (end of month 3)
- User satisfaction (NPS): > 50

---

## Next Steps

Based on project progress, prioritize:

1. **Review & Approve**: Validate architecture decisions with your team
2. **Set up infrastructure**: Create necessary accounts (Vercel, Railway/Fly.io, Supabase, OpenAI, Anthropic)
3. **Initialize codebase**: Set up monorepo structure if not already done
4. **Development sprints**: Follow the roadmap defined in `job-app-ai-roadmap.md`
5. **Weekly reviews**: Assess progress against milestones and adjust as needed

> **Tip:** Refer to [DEPLOYMENT.md](./DEPLOYMENT.md) for detailed setup instructions

---

**Document Version History:**
- v1.0 (2025-10-15): Initial design document created

**Maintained by:** Development Team
**Review Frequency:** Bi-weekly during active development, monthly post-launch

> **Related Documents:**
> - [README.md](./README.md) - Project overview and quick start
> - [API_SPEC.md](./API_SPEC.md) - Complete API reference
> - [DEPLOYMENT.md](./DEPLOYMENT.md) - Deployment and operations guide
> - [job-app-ai-roadmap.md](./job-app-ai-roadmap.md) - Development roadmap
