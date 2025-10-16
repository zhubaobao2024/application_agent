# Deployment Guide

**Version:** 1.0
**Last Updated:** 2025-10-15

> **Overview:** This guide covers development setup, environment configuration, and deployment to production. Follow the sections in order for initial setup, or jump to specific sections as needed.

---

## Table of Contents
1. [Prerequisites](#prerequisites)
2. [Development Setup](#development-setup)
3. [Environment Configuration](#environment-configuration)
4. [Database Setup](#database-setup)
5. [Deploying Frontend (Vercel)](#deploying-frontend-vercel)
6. [Deploying Backend (Railway)](#deploying-backend-railway)
7. [Alternative: Fly.io Deployment](#alternative-flyio-deployment)
8. [Post-Deployment](#post-deployment)
9. [Monitoring & Logging](#monitoring--logging)
10. [Troubleshooting](#troubleshooting)
11. [Rollback Procedures](#rollback-procedures)

---

## Prerequisites

### Required Accounts
- [ ] GitHub account (for repository hosting)
- [ ] Vercel account (frontend hosting)
- [ ] Railway or Fly.io account (backend hosting)
- [ ] Supabase account (database & auth)
- [ ] OpenAI account with API access
- [ ] Anthropic account with API access (optional but recommended)

### Required Tools
```bash
# Check if you have these installed
node --version    # v18+ required
pnpm --version    # v8+ required
python --version  # 3.11+ required
poetry --version  # 1.5+ required
docker --version  # For local development
git --version
```

### Install Missing Tools

**Node.js & pnpm:**
```bash
# Install Node.js via nvm (recommended)
curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.0/install.sh | bash
nvm install 18
nvm use 18

# Install pnpm
npm install -g pnpm
```

**Python & Poetry:**
```bash
# Install Python 3.11 (macOS)
brew install python@3.11

# Install Python 3.11 (Ubuntu)
sudo apt update
sudo apt install python3.11 python3.11-venv

# Install Poetry
curl -sSL https://install.python-poetry.org | python3 -
```

**Docker:**
```bash
# macOS
brew install --cask docker

# Ubuntu
sudo apt install docker.io docker-compose
```

---

## Development Setup

### 1. Clone Repository

```bash
git clone <your-repository-url>
cd application_agent
```

### 2. Install Dependencies

**Frontend:**
```bash
cd apps/web
pnpm install
```

**Backend:**
```bash
cd apps/api
poetry install
```

### 3. Set Up Environment Variables

**Create `.env` files:**

```bash
# Root directory
cp .env.example .env

# Frontend
cp apps/web/.env.example apps/web/.env.local

# Backend
cp apps/api/.env.example apps/api/.env
```

**Fill in environment variables** (see [Environment Configuration](#environment-configuration))

### 4. Start Local Services

**Option A: Docker Compose (Recommended)**
```bash
# Start PostgreSQL and Redis
docker-compose up -d

# This starts:
# - PostgreSQL on localhost:5432
# - Redis on localhost:6379
# - Adminer (DB GUI) on localhost:8080
```

**Option B: Manual Setup**
```bash
# PostgreSQL
brew services start postgresql@14
createdb job_app_dev

# Redis
brew services start redis
```

### 5. Run Database Migrations

```bash
# From root directory
pnpm db:migrate

# Or manually
cd apps/web
npx prisma migrate dev
```

### 6. Start Development Servers

> **Tip:** Use terminal multiplexers like `tmux` or `screen`, or separate terminal windows for each service.

**Terminal 1 - Frontend:**
```bash
cd apps/web
pnpm dev
# Runs on http://localhost:3000
```

**Terminal 2 - Backend:**
```bash
cd apps/api
poetry run uvicorn main:app --reload --port 8000
# Runs on http://localhost:8000
```

**Terminal 3 - Celery Worker (for async tasks):**
```bash
cd apps/api
poetry run celery -A worker worker --loglevel=info
```

> **Note:** If you don't need async job processing during initial development, you can skip starting the Celery worker.

### 7. Verify Setup

```bash
# Check frontend
curl http://localhost:3000/api/health

# Check backend
curl http://localhost:8000/health

# Expected response:
# {"status": "ok", "timestamp": "2024-10-15T10:00:00Z"}
```

---

## Environment Configuration

### Frontend Environment Variables

**`apps/web/.env.local`:**
```bash
# Database (Supabase)
DATABASE_URL="postgresql://user:password@db.supabase.co:5432/postgres"

# Supabase
NEXT_PUBLIC_SUPABASE_URL="https://your-project.supabase.co"
NEXT_PUBLIC_SUPABASE_ANON_KEY="eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
SUPABASE_SERVICE_ROLE_KEY="eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."

# App Configuration
NEXT_PUBLIC_APP_URL="http://localhost:3000"
NEXT_PUBLIC_API_URL="http://localhost:8000"

# Feature Flags (optional)
NEXT_PUBLIC_ENABLE_ANALYTICS=false
NEXT_PUBLIC_ENABLE_BETA_FEATURES=false
```

### Backend Environment Variables

**`apps/api/.env`:**
```bash
# Database
DATABASE_URL="postgresql://user:password@localhost:5432/job_app_dev"

# Redis
REDIS_URL="redis://localhost:6379/0"

# Supabase
SUPABASE_URL="https://your-project.supabase.co"
SUPABASE_SERVICE_KEY="eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."

# AI Services
OPENAI_API_KEY="sk-proj-..."
ANTHROPIC_API_KEY="sk-ant-..."

# Job Board APIs
LINKEDIN_EMAIL="your-email@example.com"
LINKEDIN_PASSWORD="your-secure-password"
INDEED_API_KEY="your-indeed-key"
GREENHOUSE_API_KEY="your-greenhouse-key"

# Storage (AWS S3 or compatible)
AWS_ACCESS_KEY_ID="your-access-key"
AWS_SECRET_ACCESS_KEY="your-secret-key"
AWS_S3_BUCKET="job-app-cvs"
AWS_REGION="us-east-1"

# Application Settings
APP_ENV="development"
LOG_LEVEL="DEBUG"
CORS_ORIGINS="http://localhost:3000,http://localhost:3001"

# Celery
CELERY_BROKER_URL="redis://localhost:6379/0"
CELERY_RESULT_BACKEND="redis://localhost:6379/0"

# Security
JWT_SECRET="your-super-secret-key-change-in-production"
```

### Production Environment Variables

**Additional variables for production:**
```bash
# Frontend
NEXT_PUBLIC_APP_URL="https://app.com"
NEXT_PUBLIC_API_URL="https://api.app.com"
NEXT_PUBLIC_ENABLE_ANALYTICS=true

# Monitoring
SENTRY_DSN="https://...@sentry.io/..."
NEXT_PUBLIC_POSTHOG_KEY="phc_..."
NEXT_PUBLIC_POSTHOG_HOST="https://app.posthog.com"

# Backend
APP_ENV="production"
LOG_LEVEL="INFO"
SENTRY_DSN="https://...@sentry.io/..."
```

---

## Database Setup

### 1. Create Supabase Project

1. Go to [https://supabase.com/dashboard](https://supabase.com/dashboard)
2. Click "New Project"
3. Fill in:
   - **Name:** job-app-assistant
   - **Database Password:** (generate strong password)
   - **Region:** Choose closest to your users
   - **Pricing Plan:** Free (for MVP) or Pro

4. Wait for project to be created (~2 minutes)

### 2. Get Supabase Credentials

1. Go to **Settings** → **API**
2. Copy:
   - **Project URL** → `NEXT_PUBLIC_SUPABASE_URL`
   - **anon public** key → `NEXT_PUBLIC_SUPABASE_ANON_KEY`
   - **service_role** key → `SUPABASE_SERVICE_ROLE_KEY`

3. Go to **Settings** → **Database**
4. Copy **Connection String** → `DATABASE_URL`
   - Format: `postgresql://postgres:[YOUR-PASSWORD]@db.[PROJECT-REF].supabase.co:5432/postgres`

### 3. Run Migrations

**Create migration file:**
```bash
cd apps/web
npx prisma migrate dev --name init
```

**Or apply migrations from SQL:**
```bash
# Copy schema from DESIGN.md
# Run in Supabase SQL Editor or via psql
psql $DATABASE_URL < migrations/001_initial_schema.sql
```

### 4. Set Up Row Level Security (RLS)

Run this in Supabase SQL Editor:

```sql
-- Enable RLS on all tables
ALTER TABLE user_profiles ENABLE ROW LEVEL SECURITY;
ALTER TABLE projects ENABLE ROW LEVEL SECURITY;
ALTER TABLE applications ENABLE ROW LEVEL SECURITY;
ALTER TABLE generated_cvs ENABLE ROW LEVEL SECURITY;
ALTER TABLE cover_letters ENABLE ROW LEVEL SECURITY;

-- User can only access their own data
CREATE POLICY "Users can view own profile"
  ON user_profiles FOR SELECT
  USING (auth.uid() = user_id);

CREATE POLICY "Users can update own profile"
  ON user_profiles FOR UPDATE
  USING (auth.uid() = user_id);

CREATE POLICY "Users can insert own profile"
  ON user_profiles FOR INSERT
  WITH CHECK (auth.uid() = user_id);

-- Similar policies for other tables...
```

### 5. Seed Database (Optional)

```bash
# Create seed script
cd apps/web
npx prisma db seed

# Or run custom seed
pnpm db:seed
```

---

## Deploying Frontend (Vercel)

### 1. Install Vercel CLI

```bash
pnpm add -g vercel
```

### 2. Login to Vercel

```bash
vercel login
```

### 3. Link Project

```bash
cd apps/web
vercel link
```

Follow prompts:
- **Set up and deploy?** Yes
- **Which scope?** Your account
- **Link to existing project?** No (first time) or Yes
- **Project name:** job-app-assistant
- **Directory:** `./apps/web`

### 4. Configure Environment Variables

**Via CLI:**
```bash
# Production
vercel env add NEXT_PUBLIC_SUPABASE_URL production
vercel env add NEXT_PUBLIC_SUPABASE_ANON_KEY production
vercel env add DATABASE_URL production
vercel env add SUPABASE_SERVICE_ROLE_KEY production

# Repeat for all environment variables
```

**Via Dashboard:**
1. Go to [vercel.com/dashboard](https://vercel.com/dashboard)
2. Select your project
3. Go to **Settings** → **Environment Variables**
4. Add all variables from `apps/web/.env.local`

### 5. Deploy

**Deploy to preview:**
```bash
vercel
```

**Deploy to production:**
```bash
vercel --prod
```

**Or push to GitHub (auto-deploy):**
```bash
git push origin main
# Vercel automatically deploys main branch to production
```

### 6. Configure Custom Domain (Optional)

1. Go to **Settings** → **Domains**
2. Add your domain: `app.com`
3. Follow DNS instructions
4. Add DNS records at your domain registrar:
   ```
   Type: A
   Name: @
   Value: 76.76.21.21

   Type: CNAME
   Name: www
   Value: cname.vercel-dns.com
   ```

### 7. Verify Deployment

```bash
curl https://your-project.vercel.app/api/health
```

---

## Deploying Backend (Railway)

### 1. Install Railway CLI

```bash
# macOS
brew install railway

# Or via npm
npm install -g @railway/cli
```

### 2. Login to Railway

```bash
railway login
```

### 3. Create New Project

```bash
cd apps/api
railway init
```

Follow prompts:
- **Project name:** job-app-assistant-api
- **Environment:** production

### 4. Add Services

**Add PostgreSQL (optional if using Supabase):**
```bash
railway add --database postgres
```

**Add Redis:**
```bash
railway add --database redis
```

### 5. Configure Environment Variables

**Via CLI:**
```bash
railway variables set OPENAI_API_KEY="sk-proj-..."
railway variables set ANTHROPIC_API_KEY="sk-ant-..."
railway variables set DATABASE_URL="postgresql://..."
railway variables set REDIS_URL="redis://..."
# ... add all variables from apps/api/.env
```

**Via Dashboard:**
1. Go to [railway.app/dashboard](https://railway.app/dashboard)
2. Select project → **Variables**
3. Add all environment variables

### 6. Create Dockerfile

**`apps/api/Dockerfile`:**
```dockerfile
FROM python:3.11-slim

WORKDIR /app

# Install Poetry
RUN pip install poetry

# Copy dependency files
COPY pyproject.toml poetry.lock ./

# Install dependencies
RUN poetry config virtualenvs.create false \
    && poetry install --no-dev --no-interaction --no-ansi

# Copy application code
COPY . .

# Expose port
EXPOSE 8000

# Run application
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

### 7. Deploy

```bash
# Deploy from CLI
railway up

# Or connect GitHub repo (recommended)
# 1. Go to Railway dashboard
# 2. Select project → Settings
# 3. Connect GitHub repo
# 4. Set deploy branch: main
# 5. Set root directory: apps/api
# 6. Railway auto-deploys on push
```

### 8. Get Service URL

```bash
# Get public URL
railway domain

# Example output:
# https://job-app-assistant-api-production.up.railway.app
```

### 9. Update Frontend Environment

Update Vercel environment variable:
```bash
vercel env add NEXT_PUBLIC_API_URL production
# Value: https://job-app-assistant-api-production.up.railway.app
```

### 10. Deploy Celery Worker

**Create separate service for worker:**

1. In Railway dashboard, click "New Service"
2. Select same GitHub repo
3. Set root directory: `apps/api`
4. Override start command:
   ```bash
   celery -A worker worker --loglevel=info
   ```
5. Add same environment variables

---

## Alternative: Fly.io Deployment

### 1. Install Fly CLI

```bash
curl -L https://fly.io/install.sh | sh
```

### 2. Login

```bash
fly auth login
```

### 3. Create App

```bash
cd apps/api
fly launch
```

Follow prompts:
- **App name:** job-app-assistant-api
- **Region:** Choose closest to users
- **PostgreSQL:** No (using Supabase)
- **Redis:** Yes

### 4. Configure `fly.toml`

**`apps/api/fly.toml`:**
```toml
app = "job-app-assistant-api"
primary_region = "sjc"

[build]
  dockerfile = "Dockerfile"

[env]
  PORT = "8000"
  APP_ENV = "production"

[http_service]
  internal_port = 8000
  force_https = true
  auto_stop_machines = true
  auto_start_machines = true
  min_machines_running = 1

[[services]]
  protocol = "tcp"
  internal_port = 8000

  [[services.ports]]
    port = 80
    handlers = ["http"]

  [[services.ports]]
    port = 443
    handlers = ["tls", "http"]

[[services.http_checks]]
  interval = 10000
  grace_period = "5s"
  method = "get"
  path = "/health"
  protocol = "http"
  timeout = 2000
```

### 5. Set Secrets

```bash
fly secrets set OPENAI_API_KEY="sk-proj-..."
fly secrets set ANTHROPIC_API_KEY="sk-ant-..."
fly secrets set DATABASE_URL="postgresql://..."
fly secrets set REDIS_URL="redis://..."
# ... add all secrets
```

### 6. Deploy

```bash
fly deploy
```

### 7. Scale (if needed)

```bash
# Scale to 2 instances
fly scale count 2

# Scale to larger VM
fly scale vm performance-2x
```

### 8. Get App URL

```bash
fly status
# Output: https://job-app-assistant-api.fly.dev
```

---

## Post-Deployment

### 1. Verify All Services

**Frontend health check:**
```bash
curl https://app.com/api/health
```

**Backend health check:**
```bash
curl https://api.app.com/health
```

**Database connection:**
```bash
curl https://api.app.com/health/db
```

### 2. Test Critical Flows

**Test authentication:**
```bash
curl -X POST https://app.com/api/auth/signup \
  -H "Content-Type: application/json" \
  -d '{"email":"test@example.com","password":"Test123!","fullName":"Test User"}'
```

**Test AI generation:**
```bash
# Get access token first, then:
curl -X POST https://api.app.com/api/ai/cv/generate \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"userId":"...","jobId":"...","templateId":"..."}'
```

### 3. Set Up Monitoring

**Vercel Analytics:**
- Automatically enabled for frontend
- View at [vercel.com/dashboard](https://vercel.com/dashboard)

**Railway Logs:**
```bash
railway logs
```

**Sentry (Error Tracking):**
1. Create account at [sentry.io](https://sentry.io)
2. Create new project
3. Copy DSN
4. Add to environment variables:
   ```bash
   vercel env add SENTRY_DSN production
   railway variables set SENTRY_DSN="https://...@sentry.io/..."
   ```

**PostHog (Analytics):**
1. Create account at [posthog.com](https://posthog.com)
2. Copy API key
3. Add to environment:
   ```bash
   vercel env add NEXT_PUBLIC_POSTHOG_KEY production
   vercel env add NEXT_PUBLIC_POSTHOG_HOST production
   ```

### 4. Set Up Uptime Monitoring

**UptimeRobot (Free):**
1. Go to [uptimerobot.com](https://uptimerobot.com)
2. Add monitors:
   - Frontend: `https://app.com`
   - Backend: `https://api.app.com/health`
3. Set alert contacts (email, Slack)

### 5. Database Backups

**Supabase automatic backups:**
- Free tier: Daily backups (7 days retention)
- Pro tier: Daily backups (30 days retention)
- View backups: Supabase Dashboard → Database → Backups

**Manual backup:**
```bash
# Backup
pg_dump $DATABASE_URL > backup_$(date +%Y%m%d).sql

# Restore
psql $DATABASE_URL < backup_20241015.sql
```

### 6. Set Up CI/CD

**GitHub Actions** (`.github/workflows/ci.yml`):
```yaml
name: CI/CD

on:
  push:
    branches: [main, develop]
  pull_request:
    branches: [main]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - uses: pnpm/action-setup@v2
      - uses: actions/setup-node@v3
        with:
          node-version: 18
          cache: 'pnpm'

      - name: Install dependencies
        run: pnpm install

      - name: Lint
        run: pnpm lint

      - name: Type check
        run: pnpm type-check

      - name: Test
        run: pnpm test

  deploy-frontend:
    needs: test
    if: github.ref == 'refs/heads/main'
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - uses: amondnet/vercel-action@v20
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
      - uses: actions/checkout@v3
      - uses: bervProject/railway-deploy@main
        with:
          railway_token: ${{ secrets.RAILWAY_TOKEN }}
          service: api
```

---

## Monitoring & Logging

### Application Logs

**Frontend logs (Vercel):**
```bash
# View real-time logs
vercel logs --follow

# View last 100 lines
vercel logs --limit 100
```

**Backend logs (Railway):**
```bash
# View real-time logs
railway logs --follow

# Filter by service
railway logs --service api
railway logs --service worker
```

**Backend logs (Fly.io):**
```bash
# View real-time logs
fly logs

# Last 200 lines
fly logs --lines 200
```

### Custom Logging

**Frontend (Next.js):**
```typescript
import { logger } from '@/lib/logger';

logger.info('User logged in', { userId: user.id });
logger.error('Failed to generate CV', { error, jobId });
```

**Backend (FastAPI):**
```python
import logging

logger = logging.getLogger(__name__)

logger.info(f"CV generated", extra={
    "user_id": user_id,
    "job_id": job_id,
    "generation_time": generation_time_ms
})
```

### Performance Monitoring

**Vercel Speed Insights:**
- Automatically enabled
- View: Dashboard → Project → Speed Insights

**Custom metrics:**
```typescript
// Track AI generation time
const startTime = Date.now();
const cv = await generateCV(params);
const duration = Date.now() - startTime;

analytics.track('cv_generated', {
  duration,
  model: 'gpt-4o',
  success: true
});
```

### Alerts

**Set up alerts for:**
- Error rate > 1%
- API response time > 2s
- AI generation failures > 5%
- Database connection errors
- Uptime < 99.5%

**Example: Sentry alert:**
1. Go to Sentry project
2. Alerts → Create Alert
3. Conditions: Error count > 10 in 5 minutes
4. Actions: Send email, Slack notification

---

## Troubleshooting

### Common Issues

#### 1. Database Connection Errors

**Symptom:** `ECONNREFUSED` or `Connection timeout`

**Solution:**
```bash
# Check DATABASE_URL format
echo $DATABASE_URL

# Test connection
psql $DATABASE_URL -c "SELECT 1"

# Verify Supabase project is active
# Check IP allowlist (Supabase Dashboard → Settings → Database)
```

#### 2. CORS Errors

**Symptom:** `Access-Control-Allow-Origin` error in browser

**Solution:**
```python
# apps/api/main.py
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "https://app.com",
        "https://*.vercel.app"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

#### 3. AI API Rate Limits

**Symptom:** `RateLimitError` from OpenAI/Anthropic

**Solution:**
```python
# Implement exponential backoff
from tenacity import retry, stop_after_attempt, wait_exponential

@retry(
    stop=stop_after_attempt(3),
    wait=wait_exponential(multiplier=1, min=4, max=10)
)
async def generate_cv_with_retry(...):
    return await openai.ChatCompletion.acreate(...)
```

#### 4. Build Failures

**Symptom:** Deployment fails during build

**Solution:**
```bash
# Check build logs
vercel logs --build

# Test build locally
cd apps/web
pnpm build

# Common fixes:
# - Clear cache: rm -rf .next node_modules && pnpm install
# - Check TypeScript errors: pnpm type-check
# - Verify environment variables are set
```

#### 5. Slow AI Generation

**Symptom:** CV generation takes > 10s

**Solution:**
```python
# Optimize prompt length
def truncate_job_description(description: str, max_tokens: int = 500):
    tokens = tiktoken.encode(description)
    if len(tokens) > max_tokens:
        return tiktoken.decode(tokens[:max_tokens])
    return description

# Use faster model for drafts
model = "gpt-4o-mini" if draft_mode else "gpt-4o"

# Cache common generations
@cache(ttl=3600)
async def generate_cv_cached(...):
    ...
```

---

## Rollback Procedures

### Rollback Frontend (Vercel)

**Option 1: Via Dashboard**
1. Go to Vercel Dashboard → Deployments
2. Find previous working deployment
3. Click "..." → "Promote to Production"

**Option 2: Via CLI**
```bash
# List deployments
vercel ls

# Rollback to specific deployment
vercel rollback <deployment-url>
```

**Option 3: Revert Git commit**
```bash
git revert HEAD
git push origin main
# Vercel auto-deploys reverted version
```

### Rollback Backend (Railway)

**Option 1: Via Dashboard**
1. Railway Dashboard → Deployments
2. Find previous deployment
3. Click "Redeploy"

**Option 2: Via CLI**
```bash
# Railway automatically keeps deployment history
railway up --detach

# If issues, redeploy previous commit
git revert HEAD
git push origin main
```

### Rollback Backend (Fly.io)

```bash
# List previous releases
fly releases

# Rollback to previous release
fly releases rollback
```

### Emergency Database Rollback

**From Supabase backup:**
1. Supabase Dashboard → Database → Backups
2. Select backup point
3. Click "Restore"
4. Wait 2-5 minutes

**From manual backup:**
```bash
# Drop current database (CAREFUL!)
psql $DATABASE_URL -c "DROP SCHEMA public CASCADE; CREATE SCHEMA public;"

# Restore from backup
psql $DATABASE_URL < backup_20241015.sql
```

---

## Production Checklist

**Before deploying to production, ensure all items below are completed:**

### Security
- [ ] All environment variables set in production
- [ ] API keys rotated from development keys
- [ ] HTTPS enforced on all endpoints
- [ ] CORS configured correctly
- [ ] Rate limiting enabled
- [ ] SQL injection protection (parameterized queries)
- [ ] XSS protection headers configured
- [ ] Secrets not committed to git

### Performance
- [ ] Database indexes created
- [ ] CDN configured for static assets
- [ ] Image optimization enabled
- [ ] API response caching implemented
- [ ] Database connection pooling enabled

### Monitoring
- [ ] Error tracking configured (Sentry)
- [ ] Analytics configured (PostHog)
- [ ] Uptime monitoring set up
- [ ] Log aggregation configured
- [ ] Performance monitoring enabled

### Functionality
- [ ] All critical user flows tested
- [ ] Email notifications working
- [ ] AI generation working
- [ ] Job scraping working
- [ ] PDF generation working
- [ ] File uploads working

### Documentation
- [ ] API documentation published
- [ ] User guide created
- [ ] Support email configured
- [ ] Status page set up

---

## Maintenance

### Regular Tasks

**Daily:**
- Check error rates in Sentry
- Monitor AI API costs
- Review application logs

**Weekly:**
- Update dependencies (patch versions)
- Review and clean up old jobs (> 30 days)
- Check disk space usage
- Verify backups are running

**Monthly:**
- Update dependencies (minor versions)
- Review security advisories
- Analyze performance metrics
- Review and optimize database queries
- Rotate API keys

**Quarterly:**
- Major dependency updates
- Security audit
- Performance optimization review
- Cost analysis and optimization

---

## Additional Resources

- **[README.md](./README.md)** - Project overview and features
- **[DESIGN.md](./DESIGN.md)** - System architecture and design decisions
- **[API_SPEC.md](./API_SPEC.md)** - Complete API reference
- **[job-app-ai-roadmap.md](./job-app-ai-roadmap.md)** - Development roadmap

---

**Last Updated:** 2025-10-15
**Maintained By:** Development Team

> **Feedback:** If you encounter issues not covered in this guide, please document them and share with the team to improve this documentation.
