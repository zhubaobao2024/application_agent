# Frontend Implementation Plan - AI Job Application Assistant

**Version:** 1.0
**Last Updated:** 2025-10-15
**Status:** Planning Phase

---

## Table of Contents
1. [Overview](#overview)
2. [Phase 1: Foundation & Setup](#phase-1-foundation--setup)
3. [Phase 2: Authentication Flow](#phase-2-authentication-flow)
4. [Phase 3: User Profile & Projects](#phase-3-user-profile--projects)
5. [Phase 4: Job Discovery](#phase-4-job-discovery)
6. [Phase 5: CV & Cover Letter Generation](#phase-5-cv--cover-letter-generation)
7. [Phase 6: Application Tracking](#phase-6-application-tracking)
8. [Phase 7: State Management & Data Fetching](#phase-7-state-management--data-fetching)
9. [Phase 8: UI/UX Polish](#phase-8-uiux-polish)
10. [Phase 9: Performance Optimization](#phase-9-performance-optimization)
11. [Phase 10: Testing](#phase-10-testing)
12. [Technology Stack Summary](#technology-stack-summary)
13. [Priority Order](#priority-order)

---

## Overview

Building a Next.js 14 application with TypeScript, focusing on the user-facing features for job discovery, CV generation, and application tracking.

**Tech Stack:**
- Next.js 14 with App Router
- TypeScript 5+
- Tailwind CSS + shadcn/ui
- Zustand + TanStack Query
- React Hook Form + Zod
- Supabase (Auth)

---

## Phase 1: Foundation & Setup

### 1.1 Project Infrastructure

**Tasks:**
- [ ] Set up monorepo structure in `apps/web/`
- [ ] Initialize Next.js 14 project with TypeScript
- [ ] Install and configure dependencies:
  ```bash
  pnpm add next@14 react react-dom
  pnpm add -D typescript @types/react @types/node
  pnpm add tailwindcss postcss autoprefixer
  pnpm add @tanstack/react-query zustand
  pnpm add react-hook-form zod @hookform/resolvers
  pnpm add @supabase/supabase-js
  pnpm add axios
  ```
- [ ] Configure Tailwind CSS
- [ ] Set up shadcn/ui:
  ```bash
  pnpm dlx shadcn-ui@latest init
  ```
- [ ] Configure environment variables (.env.local):
  ```env
  NEXT_PUBLIC_SUPABASE_URL=
  NEXT_PUBLIC_SUPABASE_ANON_KEY=
  NEXT_PUBLIC_API_URL=http://localhost:8000
  ```
- [ ] Configure TypeScript paths in `tsconfig.json`:
  ```json
  {
    "compilerOptions": {
      "paths": {
        "@/*": ["./app/*"],
        "@/components/*": ["./components/*"],
        "@/lib/*": ["./lib/*"],
        "@/hooks/*": ["./hooks/*"],
        "@/stores/*": ["./stores/*"]
      }
    }
  }
  ```

### 1.2 Base Layout Components

**Files to create:**
```
apps/web/
├── app/
│   ├── layout.tsx          # Root layout
│   ├── globals.css         # Global styles
│   └── page.tsx            # Landing page
├── components/
│   └── layout/
│       ├── Header.tsx
│       ├── Sidebar.tsx
│       └── Footer.tsx
```

**Tasks:**
- [ ] Create root layout with metadata:
  ```typescript
  // app/layout.tsx
  export const metadata = {
    title: 'AI Job Application Assistant',
    description: 'Automate your job search with AI'
  }
  ```
- [ ] Build Header component with:
  - Logo/branding
  - Navigation links
  - User menu dropdown
  - Mobile responsive menu
- [ ] Build Sidebar component with:
  - Dashboard navigation
  - Active route highlighting
  - Collapsible on mobile
- [ ] Create Footer component
- [ ] Set up route groups:
  - `(auth)/` - for login/signup
  - `(dashboard)/` - for app pages

---

## Phase 2: Authentication Flow

### 2.1 Auth Pages

**Files to create:**
```
app/(auth)/
├── layout.tsx              # Auth layout (centered card)
├── login/
│   └── page.tsx
└── signup/
    └── page.tsx
```

**Tasks:**
- [ ] Create auth layout with centered card design
- [ ] Build login page:
  - Email input
  - Password input
  - "Remember me" checkbox
  - Submit button
  - Link to signup
- [ ] Build signup page:
  - Full name input
  - Email input
  - Password input (with strength indicator)
  - Confirm password
  - Terms acceptance checkbox
  - Submit button
  - Link to login

### 2.2 Auth Integration

**Files to create:**
```
lib/
├── auth/
│   ├── supabase.ts         # Supabase client
│   ├── auth-helpers.ts     # Helper functions
│   └── middleware.ts       # Protected routes
stores/
└── authStore.ts            # Auth state
```

**Tasks:**
- [ ] Create Supabase client:
  ```typescript
  import { createClient } from '@supabase/supabase-js'

  export const supabase = createClient(
    process.env.NEXT_PUBLIC_SUPABASE_URL!,
    process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY!
  )
  ```
- [ ] Implement auth helpers:
  - `signUp(email, password, fullName)`
  - `signIn(email, password)`
  - `signOut()`
  - `getSession()`
  - `refreshToken()`
- [ ] Create auth store with Zustand:
  ```typescript
  interface AuthState {
    user: User | null
    session: Session | null
    setUser: (user: User | null) => void
    setSession: (session: Session | null) => void
    logout: () => void
  }
  ```
- [ ] Implement protected route middleware
- [ ] Add session persistence
- [ ] Handle token refresh

### 2.3 API Integration

**Files to create:**
```
app/api/auth/
├── signup/route.ts
├── login/route.ts
└── logout/route.ts
```

**Tasks:**
- [ ] POST `/api/auth/signup` - Create new user
- [ ] POST `/api/auth/login` - Authenticate user
- [ ] POST `/api/auth/logout` - End session
- [ ] Add JWT token to all authenticated requests
- [ ] Handle auth errors gracefully

---

## Phase 3: User Profile & Projects

### 3.1 Profile Pages

**Files to create:**
```
app/(dashboard)/profile/
├── page.tsx                # Profile overview
├── edit/
│   └── page.tsx           # Edit profile
└── projects/
    ├── page.tsx           # List projects
    ├── new/
    │   └── page.tsx       # Create project
    └── [id]/
        └── page.tsx       # Edit project
```

**Tasks:**
- [ ] Create profile overview page showing:
  - Personal information
  - Job preferences
  - Skills summary
  - Recent projects
  - Edit button
- [ ] Build profile edit page with sections:
  - Personal info (name, phone, location, URLs)
  - Job preferences (roles, locations, salary)
  - Professional summary
  - Skills management
  - Education entries
  - Work experience

### 3.2 Profile Components

**Files to create:**
```
app/(dashboard)/profile/components/
├── ProfileForm.tsx
├── SkillsManager.tsx
├── ExperienceEditor.tsx
├── EducationEditor.tsx
└── SalaryRangeSlider.tsx
```

**Tasks:**
- [ ] **ProfileForm.tsx** - Multi-section form with:
  - Form validation using Zod
  - React Hook Form integration
  - Auto-save functionality
  - Success/error states
- [ ] **SkillsManager.tsx** - Skills management:
  - Add skills with autocomplete
  - Categorize (technical/soft skills)
  - Remove skills
  - Drag to reorder
- [ ] **ExperienceEditor.tsx** - Work experience:
  - Company, title, dates
  - Rich text description
  - Achievements list
  - Add/edit/delete entries
- [ ] **EducationEditor.tsx** - Education entries:
  - Degree, institution, year
  - Honors/awards
  - Add/edit/delete entries

### 3.3 Projects Management

**Files to create:**
```
app/(dashboard)/profile/projects/components/
├── ProjectCard.tsx
├── ProjectForm.tsx
└── ProjectList.tsx
```

**Tasks:**
- [ ] Build project list view with cards
- [ ] Create ProjectCard component showing:
  - Title and description
  - Technologies as badges
  - GitHub/demo links
  - Featured badge
  - Edit/delete actions
- [ ] Build ProjectForm with fields:
  - Title, description, detailed description
  - Technologies (multi-select)
  - Role, start/end dates
  - GitHub URL, demo URL
  - Achievements (dynamic list)
  - Metrics (key-value pairs)
  - Relevance tags
  - Featured checkbox
- [ ] Add form validation
- [ ] Implement CRUD operations

### 3.4 API Integration

**Files to create:**
```
lib/api/
└── profile.ts              # Profile API functions
```

**Tasks:**
- [ ] GET `/api/profile` - Fetch user profile
- [ ] PUT `/api/profile` - Update profile
- [ ] GET `/api/profile/projects` - List projects
- [ ] POST `/api/profile/projects` - Create project
- [ ] PUT `/api/profile/projects/:id` - Update project
- [ ] DELETE `/api/profile/projects/:id` - Delete project
- [ ] Add loading states
- [ ] Handle errors with toast notifications

---

## Phase 4: Job Discovery

### 4.1 Job Pages

**Files to create:**
```
app/(dashboard)/jobs/
├── page.tsx                # Job listing
├── [id]/
│   └── page.tsx           # Job detail
└── components/
    ├── JobCard.tsx
    ├── JobFilters.tsx
    ├── JobSearch.tsx
    └── MatchScoreBadge.tsx
```

**Tasks:**
- [ ] Create job listing page with:
  - Search bar
  - Filters sidebar
  - Job cards grid
  - Pagination
  - Sort options
- [ ] Build job detail page with:
  - Full job information
  - Match analysis
  - Apply CTA
  - Similar jobs

### 4.2 Job Components

**JobCard.tsx:**
- [ ] Company logo and name
- [ ] Job title
- [ ] Location and remote type badges
- [ ] Salary range
- [ ] Required skills tags
- [ ] Match score badge
- [ ] Favorite/hide buttons
- [ ] Posted date
- [ ] Click to view details

**JobFilters.tsx:**
- [ ] Source filter (LinkedIn, Indeed, etc.)
- [ ] Location multi-select
- [ ] Remote type (remote/hybrid/onsite)
- [ ] Salary range slider
- [ ] Experience level
- [ ] Skills multi-select
- [ ] Reset filters button
- [ ] Active filters count badge

**JobSearch.tsx:**
- [ ] Search input with debounce
- [ ] Search suggestions dropdown
- [ ] Recent searches
- [ ] Clear search button

**MatchScoreBadge.tsx:**
- [ ] Visual indicator (color-coded)
- [ ] Score percentage
- [ ] Tooltip with details

### 4.3 Job Detail Page

**Sections to build:**
- [ ] Header with company info and apply CTA
- [ ] Job description (formatted HTML)
- [ ] Requirements & responsibilities
- [ ] Benefits list
- [ ] Match analysis card:
  - Overall match score
  - Matching skills (green)
  - Missing skills (red)
  - AI suggestions
- [ ] Application history (if applied)
- [ ] Similar jobs section
- [ ] Share job button

### 4.4 API Integration

**Files to create:**
```
lib/api/
└── jobs.ts                 # Jobs API functions
```

**Tasks:**
- [ ] GET `/api/jobs` with query params
- [ ] GET `/api/jobs/:id`
- [ ] POST `/api/jobs/search`
- [ ] POST `/api/jobs/:id/favorite`
- [ ] POST `/api/jobs/:id/hide`
- [ ] Implement infinite scroll for job listing
- [ ] Add optimistic updates for favorite/hide
- [ ] Cache job details

---

## Phase 5: CV & Cover Letter Generation

### 5.1 Generation Wizard

**Files to create:**
```
app/(dashboard)/generate/
├── page.tsx                # Generation wizard
└── components/
    ├── StepIndicator.tsx
    ├── JobSelector.tsx
    ├── TemplateSelector.tsx
    ├── GenerationOptions.tsx
    ├── CVPreview.tsx
    └── CoverLetterEditor.tsx
```

**Tasks:**
- [ ] Create multi-step wizard:
  - **Step 1:** Select job from favorites/recent
  - **Step 2:** Choose CV template
  - **Step 3:** Customize generation options
  - **Step 4:** Generate & preview
  - **Step 5:** Download or apply
- [ ] Add progress indicator
- [ ] Enable back/next navigation
- [ ] Save draft state

### 5.2 Generation Components

**TemplateSelector.tsx:**
- [ ] Grid of template previews
- [ ] Template name and description
- [ ] Thumbnail images
- [ ] Select/active state
- [ ] Preview modal

**CVPreview.tsx:**
- [ ] Real-time HTML rendering
- [ ] PDF preview iframe
- [ ] Download PDF button
- [ ] Edit content inline
- [ ] Regenerate button
- [ ] Version history dropdown

**CoverLetterEditor.tsx:**
- [ ] Rich text editor (Tiptap or similar)
- [ ] AI generation button
- [ ] Tone selector (professional/enthusiastic/casual)
- [ ] Key points input
- [ ] Character count
- [ ] Save as draft
- [ ] Copy to clipboard

**GenerationOptions.tsx:**
- [ ] Project selection (checkboxes)
- [ ] Skills to emphasize (multi-select)
- [ ] Tone selector
- [ ] Max length slider
- [ ] Additional instructions textarea

### 5.3 CV Management

**Files to create:**
```
app/(dashboard)/cvs/
├── page.tsx                # List all CVs
└── [id]/
    └── page.tsx           # CV detail
```

**Tasks:**
- [ ] List all generated CVs with:
  - Job information
  - Generation date
  - Template used
  - Download link
  - Regenerate option
- [ ] Show version history
- [ ] Compare versions
- [ ] Share CV via link

### 5.4 API Integration

**Files to create:**
```
lib/api/
├── ai.ts                   # AI generation API
└── cvs.ts                  # CV management API
```

**Tasks:**
- [ ] POST `/api/ai/cv/generate` (FastAPI)
- [ ] POST `/api/ai/cover-letter/generate` (FastAPI)
- [ ] POST `/api/ai/cv/analyze` (FastAPI)
- [ ] GET `/api/cvs`
- [ ] GET `/api/cvs/:id`
- [ ] GET `/api/cvs/:id/download`
- [ ] Show generation progress
- [ ] Handle generation errors
- [ ] Display cost estimate

---

## Phase 6: Application Tracking

### 6.1 Application Pages

**Files to create:**
```
app/(dashboard)/applications/
├── page.tsx                # Application dashboard
├── [id]/
│   └── page.tsx           # Application detail
└── components/
    ├── StatusPipeline.tsx
    ├── ApplicationCard.tsx
    ├── TimelineView.tsx
    ├── InterviewScheduler.tsx
    └── NotesEditor.tsx
```

**Tasks:**
- [ ] Create application dashboard with:
  - Pipeline/kanban view
  - Statistics cards
  - Recent activity
  - Upcoming interviews
- [ ] Build application detail page

### 6.2 Application Components

**StatusPipeline.tsx:**
- [ ] Kanban board with columns:
  - Draft
  - Applied
  - Interviewing
  - Offered
  - Rejected
  - Accepted
- [ ] Drag-and-drop to change status
- [ ] Card count per column
- [ ] Add application button

**ApplicationCard.tsx:**
- [ ] Job title and company
- [ ] Applied date
- [ ] Current status badge
- [ ] Next action (e.g., "Follow up on Oct 21")
- [ ] Click to view details
- [ ] Quick actions menu

**TimelineView.tsx:**
- [ ] Chronological activity list
- [ ] Event types (applied, interview, status change)
- [ ] Timestamps
- [ ] Notes attached to events

**InterviewScheduler.tsx:**
- [ ] Interview type selector (phone/video/onsite)
- [ ] Date/time picker
- [ ] Location/meeting link
- [ ] Notes field
- [ ] Calendar integration

**NotesEditor.tsx:**
- [ ] Rich text editor
- [ ] Attachments support
- [ ] Auto-save
- [ ] Timestamps

### 6.3 Dashboard Home

**Files to create:**
```
app/(dashboard)/
└── page.tsx                # Dashboard home
```

**Tasks:**
- [ ] Statistics cards:
  - Total applications
  - Interviews scheduled
  - Offers received
  - Response rate
- [ ] Recent activity feed
- [ ] Upcoming interviews list
- [ ] Action items (follow-ups due)
- [ ] Quick actions (generate CV, search jobs)

### 6.4 API Integration

**Files to create:**
```
lib/api/
└── applications.ts         # Applications API functions
```

**Tasks:**
- [ ] GET `/api/applications`
- [ ] POST `/api/applications`
- [ ] PUT `/api/applications/:id`
- [ ] DELETE `/api/applications/:id`
- [ ] Optimistic updates for status changes
- [ ] Real-time updates (optional)

---

## Phase 7: State Management & Data Fetching

### 7.1 Zustand Stores

**Files to create:**
```
stores/
├── authStore.ts            # User session
├── jobFiltersStore.ts      # Job filters state
└── uiStore.ts              # UI preferences
```

**Tasks:**
- [ ] **authStore.ts:**
  ```typescript
  interface AuthState {
    user: User | null
    profile: UserProfile | null
    session: Session | null
    setUser: (user: User | null) => void
    setProfile: (profile: UserProfile | null) => void
    logout: () => void
  }
  ```
- [ ] **jobFiltersStore.ts:**
  ```typescript
  interface JobFiltersState {
    filters: JobFilters
    setFilters: (filters: JobFilters) => void
    resetFilters: () => void
  }
  ```
- [ ] **uiStore.ts:**
  ```typescript
  interface UIState {
    sidebarOpen: boolean
    theme: 'light' | 'dark'
    notifications: Notification[]
    setSidebarOpen: (open: boolean) => void
    setTheme: (theme: 'light' | 'dark') => void
    addNotification: (notification: Notification) => void
  }
  ```
- [ ] Persist filters and preferences to localStorage

### 7.2 TanStack Query Setup

**Files to create:**
```
lib/
├── queryClient.ts          # Query client config
└── hooks/
    ├── useJobs.ts
    ├── useProfile.ts
    ├── useApplications.ts
    └── useCVs.ts
```

**Tasks:**
- [ ] Configure QueryClient:
  ```typescript
  export const queryClient = new QueryClient({
    defaultOptions: {
      queries: {
        staleTime: 5 * 60 * 1000, // 5 minutes
        cacheTime: 10 * 60 * 1000, // 10 minutes
        refetchOnWindowFocus: false,
        retry: 1,
      },
    },
  })
  ```
- [ ] Create query hooks:
  - `useJobs(filters)` - List jobs
  - `useJob(id)` - Get job details
  - `useProfile()` - Get user profile
  - `useProjects()` - List projects
  - `useApplications(filters)` - List applications
  - `useCVs()` - List generated CVs
- [ ] Create mutation hooks:
  - `useGenerateCV()` - Generate CV
  - `useGenerateCoverLetter()` - Generate cover letter
  - `useCreateApplication()` - Create application
  - `useUpdateApplication()` - Update application
  - `useCreateProject()` - Create project
- [ ] Implement optimistic updates
- [ ] Configure cache invalidation
- [ ] Add error handling

### 7.3 API Client Layer

**Files to create:**
```
lib/api/
├── client.ts               # Axios instance
└── interceptors.ts         # Request/response interceptors
```

**Tasks:**
- [ ] Create axios instance:
  ```typescript
  export const apiClient = axios.create({
    baseURL: process.env.NEXT_PUBLIC_API_URL,
    timeout: 30000,
  })
  ```
- [ ] Add request interceptor:
  - Attach JWT token to headers
  - Add request ID
  - Log requests (dev mode)
- [ ] Add response interceptor:
  - Handle 401 (refresh token)
  - Transform response data
  - Handle errors globally
  - Log responses (dev mode)
- [ ] Implement retry logic
- [ ] Add request cancellation

---

## Phase 8: UI/UX Polish

### 8.1 Shared Components

**Install shadcn/ui components:**
```bash
pnpm dlx shadcn-ui@latest add button
pnpm dlx shadcn-ui@latest add input
pnpm dlx shadcn-ui@latest add select
pnpm dlx shadcn-ui@latest add checkbox
pnpm dlx shadcn-ui@latest add card
pnpm dlx shadcn-ui@latest add badge
pnpm dlx shadcn-ui@latest add avatar
pnpm dlx shadcn-ui@latest add dialog
pnpm dlx shadcn-ui@latest add dropdown-menu
pnpm dlx shadcn-ui@latest add tabs
pnpm dlx shadcn-ui@latest add toast
pnpm dlx shadcn-ui@latest add skeleton
```

**Files to create:**
```
components/
├── ui/                     # shadcn/ui components
├── layout/
│   ├── Header.tsx
│   ├── Sidebar.tsx
│   └── Footer.tsx
└── shared/
    ├── LoadingSpinner.tsx
    ├── LoadingSkeleton.tsx
    ├── ErrorBoundary.tsx
    ├── ErrorState.tsx
    ├── EmptyState.tsx
    ├── Pagination.tsx
    └── SearchBar.tsx
```

**Tasks:**
- [ ] Customize shadcn/ui theme
- [ ] Create reusable loading states
- [ ] Build error boundary component
- [ ] Create empty state component
- [ ] Build pagination component
- [ ] Add toast notification system

### 8.2 Form Validation

**Files to create:**
```
lib/validations/
├── auth.ts                 # Auth form schemas
├── profile.ts              # Profile form schemas
├── project.ts              # Project form schemas
└── application.ts          # Application form schemas
```

**Tasks:**
- [ ] Create Zod schemas for all forms:
  ```typescript
  // lib/validations/auth.ts
  export const loginSchema = z.object({
    email: z.string().email('Invalid email address'),
    password: z.string().min(8, 'Password must be at least 8 characters'),
  })
  ```
- [ ] Integrate with React Hook Form:
  ```typescript
  const form = useForm({
    resolver: zodResolver(loginSchema),
  })
  ```
- [ ] Add field-level validation
- [ ] Display inline error messages
- [ ] Add success states
- [ ] Disable submit during validation

### 8.3 Error Handling

**Files to create:**
```
components/shared/
├── ErrorBoundary.tsx
├── ErrorState.tsx
└── ToastProvider.tsx
```

**Tasks:**
- [ ] Create global error boundary
- [ ] Handle API errors with toast
- [ ] Add retry buttons
- [ ] Create fallback UI
- [ ] Log errors to monitoring service (Sentry)

### 8.4 Loading States

**Tasks:**
- [ ] Skeleton loaders for:
  - Job cards
  - Profile forms
  - Application cards
  - Dashboard stats
- [ ] Spinners for buttons
- [ ] Progress bars for CV generation
- [ ] Optimistic UI updates
- [ ] Suspense boundaries

---

## Phase 9: Performance Optimization

### 9.1 Code Splitting

**Tasks:**
- [ ] Dynamic imports for heavy components:
  ```typescript
  const CVPreview = dynamic(() => import('@/components/CVPreview'), {
    loading: () => <LoadingSkeleton />
  })
  ```
- [ ] Route-based code splitting (automatic with App Router)
- [ ] Lazy load modals and dialogs
- [ ] Split vendor bundles

### 9.2 Image Optimization

**Tasks:**
- [ ] Use Next.js Image component everywhere
- [ ] Optimize company logos:
  ```typescript
  <Image
    src={job.companyLogoUrl}
    alt={job.company}
    width={48}
    height={48}
    loading="lazy"
  />
  ```
- [ ] Add blur placeholders
- [ ] Lazy load images below fold

### 9.3 Caching Strategy

**Tasks:**
- [ ] Configure TanStack Query cache:
  - Job listings: 5 minutes stale time
  - Job details: 10 minutes
  - Profile: Cache indefinitely, invalidate on update
  - Applications: Real-time or short stale time
- [ ] Implement background refetching
- [ ] Add prefetching for common routes:
  ```typescript
  queryClient.prefetchQuery(['jobs', filters])
  ```

### 9.4 SEO & Metadata

**Tasks:**
- [ ] Add dynamic metadata for job pages:
  ```typescript
  export async function generateMetadata({ params }) {
    const job = await getJob(params.id)
    return {
      title: `${job.title} at ${job.company}`,
      description: job.description.slice(0, 160),
    }
  }
  ```
- [ ] Add Open Graph tags
- [ ] Add structured data (JSON-LD) for jobs
- [ ] Create sitemap
- [ ] Add robots.txt

---

## Phase 10: Testing

### 10.1 Unit Tests (Vitest)

**Setup:**
```bash
pnpm add -D vitest @testing-library/react @testing-library/jest-dom
```

**Files to create:**
```
__tests__/
├── lib/
│   ├── utils.test.ts
│   └── validations.test.ts
└── hooks/
    └── useJobs.test.ts
```

**Tasks:**
- [ ] Test utility functions
- [ ] Test form validation schemas
- [ ] Test custom hooks
- [ ] Test API client functions
- [ ] Aim for >80% coverage

### 10.2 Component Tests

**Files to create:**
```
__tests__/components/
├── JobCard.test.tsx
├── ProfileForm.test.tsx
└── ApplicationCard.test.tsx
```

**Tasks:**
- [ ] Test UI components render correctly
- [ ] Test form submissions
- [ ] Test error states
- [ ] Test loading states
- [ ] Test user interactions

### 10.3 E2E Tests (Playwright)

**Setup:**
```bash
pnpm add -D @playwright/test
```

**Files to create:**
```
e2e/
├── auth.spec.ts
├── jobs.spec.ts
├── cv-generation.spec.ts
└── applications.spec.ts
```

**Tasks:**
- [ ] Test complete auth flow (signup, login, logout)
- [ ] Test job search and filtering
- [ ] Test CV generation flow
- [ ] Test application creation and tracking
- [ ] Test profile editing
- [ ] Run on CI/CD pipeline

---

## Technology Stack Summary

### Core Technologies
```typescript
{
  "framework": "Next.js 14 (App Router)",
  "language": "TypeScript 5+",
  "runtime": "React 18",
  "styling": "Tailwind CSS",
  "ui": "shadcn/ui"
}
```

### State Management
```typescript
{
  "global": "Zustand",
  "server": "TanStack Query",
  "forms": "React Hook Form"
}
```

### Data & API
```typescript
{
  "validation": "Zod",
  "http": "Axios",
  "auth": "Supabase",
  "backend": "FastAPI (Python)"
}
```

### Development Tools
```typescript
{
  "packageManager": "pnpm",
  "linting": "ESLint",
  "formatting": "Prettier",
  "unitTests": "Vitest",
  "e2eTests": "Playwright"
}
```

---

## Key Files Structure

```
apps/web/
├── app/
│   ├── layout.tsx
│   ├── page.tsx
│   ├── globals.css
│   │
│   ├── (auth)/
│   │   ├── layout.tsx
│   │   ├── login/page.tsx
│   │   └── signup/page.tsx
│   │
│   ├── (dashboard)/
│   │   ├── layout.tsx
│   │   ├── page.tsx (dashboard home)
│   │   │
│   │   ├── jobs/
│   │   │   ├── page.tsx
│   │   │   ├── [id]/page.tsx
│   │   │   └── components/
│   │   │
│   │   ├── applications/
│   │   │   ├── page.tsx
│   │   │   ├── [id]/page.tsx
│   │   │   └── components/
│   │   │
│   │   ├── profile/
│   │   │   ├── page.tsx
│   │   │   ├── edit/page.tsx
│   │   │   ├── projects/
│   │   │   └── components/
│   │   │
│   │   ├── generate/
│   │   │   ├── page.tsx
│   │   │   └── components/
│   │   │
│   │   └── cvs/
│   │       ├── page.tsx
│   │       └── [id]/page.tsx
│   │
│   └── api/
│       └── (Next.js API routes)
│
├── components/
│   ├── ui/                 # shadcn/ui components
│   ├── layout/
│   │   ├── Header.tsx
│   │   ├── Sidebar.tsx
│   │   └── Footer.tsx
│   └── shared/
│       ├── LoadingSpinner.tsx
│       ├── ErrorBoundary.tsx
│       └── EmptyState.tsx
│
├── lib/
│   ├── api/
│   │   ├── client.ts
│   │   ├── jobs.ts
│   │   ├── profile.ts
│   │   ├── applications.ts
│   │   ├── cvs.ts
│   │   └── ai.ts
│   ├── auth/
│   │   ├── supabase.ts
│   │   └── auth-helpers.ts
│   ├── validations/
│   │   ├── auth.ts
│   │   ├── profile.ts
│   │   └── application.ts
│   ├── utils/
│   └── queryClient.ts
│
├── stores/
│   ├── authStore.ts
│   ├── jobFiltersStore.ts
│   └── uiStore.ts
│
├── hooks/
│   ├── useJobs.ts
│   ├── useProfile.ts
│   ├── useApplications.ts
│   └── useCVs.ts
│
├── types/
│   ├── job.ts
│   ├── profile.ts
│   ├── application.ts
│   └── cv.ts
│
├── __tests__/
│   ├── lib/
│   ├── components/
│   └── hooks/
│
└── e2e/
    ├── auth.spec.ts
    └── jobs.spec.ts
```

---

## Priority Order

### MVP Features (Phase 1) - 4-6 weeks

**Week 1-2:**
1. ✅ Project setup and infrastructure
2. ✅ Authentication flow (login/signup)
3. ✅ Basic layouts and navigation
4. ✅ API client setup

**Week 3-4:**
5. ✅ Profile management (view/edit)
6. ✅ Project management (CRUD)
7. ✅ Job listing and search
8. ✅ Job detail page

**Week 5-6:**
9. ✅ Basic CV generation
10. ✅ Application tracking (list/create)
11. ✅ Dashboard home page

### Phase 2 Features - 3-4 weeks

**Week 7-8:**
1. ✅ Advanced job filters
2. ✅ Match scoring display
3. ✅ Cover letter generation
4. ✅ CV template selection

**Week 9-10:**
5. ✅ Application pipeline (Kanban)
6. ✅ Interview scheduling
7. ✅ Notes and timeline
8. ✅ Favorite/hide jobs

### Phase 3 Features - 2-3 weeks

**Week 11-12:**
1. ✅ Dashboard analytics
2. ✅ Advanced application tracking
3. ✅ Notifications
4. ✅ Mobile optimization

**Week 13:**
5. ✅ Performance optimization
6. ✅ Testing (E2E)
7. ✅ Bug fixes and polish

---

## Implementation Checklist

### Before Starting
- [ ] Review DESIGN.md and API_SPEC.md thoroughly
- [ ] Set up development environment
- [ ] Create Supabase project
- [ ] Obtain API keys (OpenAI/Anthropic)
- [ ] Set up version control

### During Development
- [ ] Follow TypeScript best practices
- [ ] Write clean, maintainable code
- [ ] Add comments for complex logic
- [ ] Keep components small and focused
- [ ] Use consistent naming conventions
- [ ] Test as you build
- [ ] Commit frequently with clear messages

### Before Launch
- [ ] Complete all MVP features
- [ ] Fix critical bugs
- [ ] Optimize performance
- [ ] Run E2E tests
- [ ] Security audit
- [ ] Accessibility check
- [ ] Deploy to staging
- [ ] User acceptance testing

---

## Next Steps

1. **Review & Validate**: Review this plan with your team
2. **Set Up Environment**: Create necessary accounts and API keys
3. **Initialize Project**: Set up Next.js project and install dependencies
4. **Start Phase 1**: Begin with authentication and layout components
5. **Iterate**: Build incrementally, test frequently, and gather feedback

---

**Document maintained by:** Frontend Development Team
**Review frequency:** Weekly during active development
**Related documents:**
- [README.md](./README.md)
- [DESIGN.md](./DESIGN.md)
- [API_SPEC.md](./API_SPEC.md)
