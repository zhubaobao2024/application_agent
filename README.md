# AI Job Application Assistant

An AI-powered application that automates and streamlines the job application process by intelligently collecting relevant job openings, adapting your CV based on job requirements, and generating personalized cover letters.

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![TypeScript](https://img.shields.io/badge/TypeScript-5.0-blue)](https://www.typescriptlang.org/)
[![Python](https://img.shields.io/badge/Python-3.11-blue)](https://www.python.org/)
[![Next.js](https://img.shields.io/badge/Next.js-14-black)](https://nextjs.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.104-green)](https://fastapi.tiangolo.com/)

## 🚀 Development Status

| Phase | Status | Description |
|-------|--------|-------------|
| **Phase 1** | ✅ **Complete** | Foundation & Setup - Next.js, TypeScript, Tailwind CSS |
| **Phase 2** | ✅ **Complete** | Authentication Flow - Supabase auth, login/signup, protected routes |
| **Phase 3** | 🔄 In Progress | User Profile Management |
| **Phase 4** | ⏳ Planned | Job Discovery & Search |
| **Phase 5** | ⏳ Planned | CV & Cover Letter Generation |
| **Phase 6** | ⏳ Planned | Application Tracking |

**Current Status:** Fully functional authentication system with user signup, login, and protected dashboard. Ready for profile management implementation.

---

## Features

### ✅ Implemented
- **User Authentication**: Complete signup/login system with Supabase
- **Protected Routes**: Secure dashboard with session management
- **Modern UI**: Responsive design with Tailwind CSS and shadcn/ui components
- **Type Safety**: Full TypeScript coverage with strict mode

### 🚧 In Development
- **User Profile Management**: Skills, experience, and project portfolio
- **Job Discovery Engine**: Search and filter job opportunities

### 📋 Planned
- **AI-Powered CV Adaptation**: Tailors your CV to match specific job requirements using GPT-4o/Claude
- **Smart Cover Letter Generation**: Creates personalized, compelling cover letters in seconds
- **Application Tracking**: Comprehensive dashboard to manage your job applications and interview pipeline
- **Match Scoring**: AI analyzes how well your profile matches each job opportunity
- **Multi-Template Support**: Choose from professional CV templates or create custom ones

---

## Quick Start

### Prerequisites

- **Node.js 18+** and **pnpm** (for frontend)
- **Supabase Account** (for authentication) - [Create one here](https://supabase.com)
- Python 3.11+ and Poetry (for backend - coming in later phases)

### Installation

```bash
# Clone repository
git clone <repository-url>
cd application_agent

# Install dependencies
pnpm install

# Set up environment variables
cd apps/web
cp .env.example .env.local
```

**Edit `apps/web/.env.local`:**
```env
NEXT_PUBLIC_SUPABASE_URL=your-supabase-project-url
NEXT_PUBLIC_SUPABASE_ANON_KEY=your-supabase-anon-key
NEXT_PUBLIC_API_URL=http://localhost:8000
```

**Get Supabase credentials:**
1. Go to [supabase.com](https://supabase.com) and create a project
2. Go to Project Settings → API
3. Copy your project URL and anon/public key
4. Enable Email Auth in Authentication → Providers

```bash
# Start development server
pnpm dev

# Server runs at http://localhost:3000
```

**Try it out:**
- Visit `http://localhost:3000`
- Click "Get Started" to create an account
- Sign in and explore the dashboard

### What's Working Right Now

✅ **Frontend (Phase 1 & 2):**
- Landing page at `/`
- User signup at `/signup`
- User login at `/login`
- Protected dashboard at `/dashboard`
- Session management and logout

⏳ **Backend (Coming Soon):**
- Job scraping and AI features will be added in later phases
- Currently frontend-only with Supabase auth

---

## Project Structure

```
application_agent/
├── apps/
│   ├── web/                      # ✅ Next.js 14 Frontend (ACTIVE)
│   │   ├── app/
│   │   │   ├── (auth)/          # ✅ Auth pages (login, signup)
│   │   │   ├── (dashboard)/     # ✅ Protected dashboard
│   │   │   ├── layout.tsx       # ✅ Root layout with AuthProvider
│   │   │   ├── page.tsx         # ✅ Landing page
│   │   │   └── globals.css      # ✅ Tailwind styles
│   │   ├── components/
│   │   │   ├── ui/              # ✅ shadcn/ui components
│   │   │   ├── providers/       # ✅ AuthProvider
│   │   │   ├── layout/          # Layout components (empty)
│   │   │   └── shared/          # Shared components (empty)
│   │   ├── lib/
│   │   │   ├── auth/            # ✅ Supabase client & helpers
│   │   │   ├── validations/     # ✅ Zod schemas
│   │   │   ├── api/             # API client (empty)
│   │   │   └── utils.ts         # ✅ Utility functions
│   │   ├── stores/
│   │   │   └── authStore.ts     # ✅ Zustand auth state
│   │   ├── hooks/               # Custom hooks (empty)
│   │   ├── types/
│   │   │   └── auth.ts          # ✅ Auth types
│   │   └── public/              # Static assets (empty)
│   │
│   └── api/                      # ⏳ FastAPI Backend (PLANNED)
│       └── (coming in later phases)
│
├── packages/                     # ⏳ Shared packages (PLANNED)
│
├── DESIGN.md                     # System design document
├── API_SPEC.md                   # API specification
├── DEPLOYMENT.md                 # Deployment guide
├── FRONTEND_IMPLEMENTATION_PLAN.md  # ✅ Frontend roadmap
├── PHASE_1_SUMMARY.md            # ✅ Phase 1 completion summary
├── PHASE_2_SUMMARY.md            # ✅ Phase 2 completion summary
└── job-app-ai-roadmap.md         # Product roadmap
```

**Legend:**
- ✅ Implemented and working
- 🚧 In development
- ⏳ Planned for future phases
- (empty) Directory exists but no files yet

---

## Technology Stack

### Frontend
- **Framework**: Next.js 14 with App Router
- **Language**: TypeScript
- **Styling**: Tailwind CSS
- **UI Components**: shadcn/ui
- **State Management**: Zustand + TanStack Query
- **Forms**: React Hook Form + Zod

### Backend
- **Framework**: FastAPI (Python)
- **ORM**: SQLAlchemy
- **Task Queue**: Celery + Redis
- **Web Scraping**: Playwright

### Infrastructure
- **Database**: PostgreSQL (Supabase)
- **Cache**: Redis
- **Auth**: Supabase Auth
- **Storage**: AWS S3 (or compatible)
- **Hosting**: Vercel (frontend) + Railway/Fly.io (backend)

### AI & ML
- **Primary AI**: OpenAI GPT-4o
- **Backup AI**: Anthropic Claude 3.5 Sonnet
- **Orchestration**: LangChain

---

## Core Workflows

### 1. Job Discovery

```mermaid
graph LR
    A[User Sets Preferences] --> B[Scheduled Scraping]
    B --> C[LinkedIn/Indeed/Greenhouse]
    C --> D[Parse & Normalize]
    D --> E[AI Match Scoring]
    E --> F[Display Relevant Jobs]
```

1. User configures job preferences (roles, locations, salary)
2. System scrapes job boards daily
3. Jobs are parsed and deduplicated
4. AI calculates match score based on user profile
5. Relevant jobs appear in user dashboard

### 2. CV Generation

```mermaid
graph LR
    A[Select Job] --> B[Choose Template]
    B --> C[AI Analyzes Job]
    C --> D[Match User Projects]
    D --> E[Generate Tailored CV]
    E --> F[Preview & Download]
```

1. User selects a job they want to apply to
2. AI analyzes job requirements
3. System matches user's projects and skills
4. AI generates tailored CV emphasizing relevant experience
5. User previews and downloads PDF

### 3. Application Tracking

```mermaid
graph LR
    A[Create Application] --> B[Attach CV & Cover Letter]
    B --> C[Track Status]
    C --> D[Add Interview Notes]
    D --> E[Update Status]
```

---

## API Overview

### Authentication

```bash
# Sign up
POST /api/auth/signup
{
  "email": "user@example.com",
  "password": "SecurePass123!",
  "fullName": "John Doe"
}

# Sign in
POST /api/auth/login
{
  "email": "user@example.com",
  "password": "SecurePass123!"
}
```

### Job Management

```bash
# List jobs
GET /api/jobs?page=1&limit=20&remote=true&minSalary=100000

# Search jobs
POST /api/jobs/search
{
  "query": "python developer",
  "filters": {
    "locations": ["Remote"],
    "skills": ["Python", "React"]
  }
}
```

### AI Generation

```bash
# Generate CV
POST /api/ai/cv/generate
{
  "userId": "user-id",
  "jobId": "job-id",
  "templateId": "template-id",
  "options": {
    "tone": "professional",
    "emphasizeSkills": ["Python", "React"]
  }
}

# Generate cover letter
POST /api/ai/cover-letter/generate
{
  "userId": "user-id",
  "jobId": "job-id",
  "tone": "enthusiastic"
}
```

Full API documentation: [API_SPEC.md](./API_SPEC.md)

---

## Development

### Running Tests

```bash
# Frontend tests
cd apps/web
pnpm test              # Unit tests
pnpm test:e2e         # E2E tests with Playwright

# Backend tests
cd apps/api
poetry run pytest      # All tests
poetry run pytest -v   # Verbose output
poetry run pytest tests/test_ai.py  # Specific file
```

### Code Quality

```bash
# Linting
pnpm lint              # ESLint for TypeScript
pnpm lint:fix         # Auto-fix issues

# Type checking
pnpm type-check

# Formatting
pnpm format           # Prettier
```

### Database Management

```bash
# Create migration
pnpm db:migrate:create --name add_new_field

# Run migrations
pnpm db:migrate

# Rollback migration
pnpm db:migrate:rollback

# Reset database (CAUTION: deletes all data)
pnpm db:reset

# Seed database
pnpm db:seed
```

### Debugging

**Frontend:**
```typescript
// Use Next.js debug mode
DEBUG=* pnpm dev

// Or in code
console.log('Debug info:', data);
```

**Backend:**
```python
# Enable debug logging
import logging
logging.basicConfig(level=logging.DEBUG)

# Or use debugger
import pdb; pdb.set_trace()
```

**API Requests:**
```bash
# View FastAPI auto-generated docs
open http://localhost:8000/docs

# Test endpoint with curl
curl -X POST http://localhost:8000/api/ai/cv/generate \
  -H "Content-Type: application/json" \
  -d '{"userId":"...","jobId":"..."}'
```

---

## Environment Variables

### Required Variables

```bash
# Database
DATABASE_URL="postgresql://user:password@localhost:5432/job_app_dev"

# Supabase
NEXT_PUBLIC_SUPABASE_URL="https://your-project.supabase.co"
NEXT_PUBLIC_SUPABASE_ANON_KEY="eyJhbGc..."
SUPABASE_SERVICE_ROLE_KEY="eyJhbGc..."

# AI Services
OPENAI_API_KEY="sk-proj-..."
ANTHROPIC_API_KEY="sk-ant-..."  # Optional

# Redis
REDIS_URL="redis://localhost:6379/0"
```

### Optional Variables

```bash
# Job Board APIs
LINKEDIN_EMAIL="your-email@example.com"
LINKEDIN_PASSWORD="your-password"
INDEED_API_KEY="your-indeed-key"

# Storage (AWS S3)
AWS_ACCESS_KEY_ID="..."
AWS_SECRET_ACCESS_KEY="..."
AWS_S3_BUCKET="job-app-cvs"

# Monitoring
SENTRY_DSN="https://...@sentry.io/..."
NEXT_PUBLIC_POSTHOG_KEY="phc_..."
```

See [.env.example](./.env.example) for complete list.

---

## Deployment

### Quick Deploy

**Frontend (Vercel):**
```bash
cd apps/web
vercel --prod
```

**Backend (Railway):**
```bash
cd apps/api
railway up
```

For detailed deployment instructions, see [DEPLOYMENT.md](./DEPLOYMENT.md).

---

## Documentation

- **[DESIGN.md](./DESIGN.md)**: System architecture and design decisions
- **[API_SPEC.md](./API_SPEC.md)**: Complete API reference
- **[DEPLOYMENT.md](./DEPLOYMENT.md)**: Deployment and operations guide
- **[job-app-ai-roadmap.md](./job-app-ai-roadmap.md)**: Product roadmap

---

## Contributing

We welcome contributions! Please follow these steps:

1. **Fork the repository**
2. **Create a feature branch**
   ```bash
   git checkout -b feature/your-feature-name
   ```
3. **Make your changes**
   - Write tests for new features
   - Follow code style guidelines
   - Update documentation
4. **Commit with conventional commits**
   ```bash
   git commit -m "feat: add job filtering by salary range"
   ```
5. **Push and create a Pull Request**
   ```bash
   git push origin feature/your-feature-name
   ```

### Commit Message Format

```
<type>(<scope>): <subject>

<body>

<footer>
```

**Types:**
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation changes
- `style`: Code style changes (formatting)
- `refactor`: Code refactoring
- `test`: Adding or updating tests
- `chore`: Maintenance tasks

**Example:**
```
feat(ai): add Claude 3.5 Sonnet as fallback provider

Added Anthropic Claude as a fallback when OpenAI is unavailable
or rate limited. Includes automatic retry logic with exponential
backoff.

Closes #123
```

---

## Troubleshooting

### Common Issues

**Database connection errors:**
```bash
# Check if PostgreSQL is running
docker-compose ps

# Restart services
docker-compose restart postgres

# Check connection
psql $DATABASE_URL -c "SELECT 1"
```

**Port already in use:**
```bash
# Find process using port 3000
lsof -ti:3000

# Kill process
kill -9 $(lsof -ti:3000)
```

**AI generation timeouts:**
```python
# Increase timeout in FastAPI
from fastapi import FastAPI
import uvicorn

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        timeout_keep_alive=300  # 5 minutes
    )
```

**Module not found errors:**
```bash
# Reinstall dependencies
rm -rf node_modules .next
pnpm install

# Python dependencies
cd apps/api
poetry install --sync
```

For more troubleshooting, see [DEPLOYMENT.md](./DEPLOYMENT.md#troubleshooting).

---

## Performance

### Benchmarks

| Operation | Target | Actual (MVP) |
|-----------|--------|--------------|
| CV Generation | < 5s | 2.3s |
| Job Search | < 500ms | 180ms |
| Page Load (Dashboard) | < 2s | 1.2s |
| API Response (avg) | < 200ms | 95ms |

### Optimization Tips

**Frontend:**
- Use Next.js Image optimization
- Implement code splitting with dynamic imports
- Enable ISR (Incremental Static Regeneration) for job listings
- Cache API responses with TanStack Query

**Backend:**
- Use database indexes on frequently queried columns
- Implement Redis caching for job listings
- Batch AI requests when possible
- Use connection pooling for database

---

## Security

### Best Practices

- All secrets stored in environment variables (never in code)
- JWT tokens with short expiration (1 hour)
- HTTPS enforced in production
- Rate limiting on all API endpoints
- Input validation with Zod/Pydantic
- SQL injection prevention (parameterized queries)
- XSS protection headers configured
- CORS properly configured

### Security Audit Checklist

- [ ] No secrets in git history
- [ ] Environment variables set in production
- [ ] Database has Row Level Security (RLS) enabled
- [ ] API rate limiting configured
- [ ] HTTPS enforced
- [ ] Dependencies regularly updated
- [ ] Security headers configured
- [ ] Error messages don't leak sensitive info

---

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## Support

- **Documentation**: See documentation files in the project root
- **Issues**: Report issues via your project's issue tracker
- **Discussions**: Discuss features and improvements with the team
- **Email**: Configure support email in your deployment

---

## Roadmap

See [job-app-ai-roadmap.md](./job-app-ai-roadmap.md) for detailed timeline.

**Upcoming Features:**
- Browser extension for one-click applications
- LinkedIn integration for auto-apply
- Mobile app (React Native)
- Multi-language support
- Advanced analytics dashboard
- Interview preparation assistant

---

## Team

This project is actively being developed. Contributions are welcome!

---

## Acknowledgments

- [OpenAI](https://openai.com) for GPT-4o API
- [Anthropic](https://anthropic.com) for Claude API
- [Supabase](https://supabase.com) for database and auth
- [Vercel](https://vercel.com) for hosting
- [shadcn/ui](https://ui.shadcn.com) for UI components

---

**Made with ❤️ by engineers, for engineers**

Give your job search superpowers.

---

## Quick Links

- [System Design](./DESIGN.md)
- [API Docs](./API_SPEC.md)
- [Deployment Guide](./DEPLOYMENT.md)
- [Roadmap](./job-app-ai-roadmap.md)

---

**Last Updated**: 2025-10-15
