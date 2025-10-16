# API Specification

**Version:** 1.0
**Base URL (Development):** `http://localhost:3000/api` (Next.js), `http://localhost:8000` (FastAPI)
**Base URL (Production):** Configure based on your deployment (e.g., `https://yourdomain.com/api`, `https://api.yourdomain.com`)

> **Note:** Replace placeholder URLs (`app.com`, `api.app.com`) with your actual domain names after deployment.

---

## Table of Contents
1. [Authentication](#authentication)
2. [Next.js API Routes](#nextjs-api-routes)
3. [FastAPI Routes](#fastapi-routes)
4. [Error Handling](#error-handling)
5. [Rate Limiting](#rate-limiting)
6. [Webhooks](#webhooks)

---

## Authentication

All authenticated endpoints require a JWT token from Supabase.

### Headers
```http
Authorization: Bearer <supabase_jwt_token>
Content-Type: application/json
```

### Authentication Flow

#### Sign Up
```http
POST /api/auth/signup
```

**Request Body:**
```json
{
  "email": "john@example.com",
  "password": "SecurePass123!",
  "fullName": "John Doe"
}
```

**Response (201 Created):**
```json
{
  "user": {
    "id": "550e8400-e29b-41d4-a716-446655440000",
    "email": "john@example.com",
    "emailConfirmed": false
  },
  "session": {
    "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
    "refresh_token": "...",
    "expires_at": 1729000000
  }
}
```

#### Sign In
```http
POST /api/auth/login
```

**Request Body:**
```json
{
  "email": "john@example.com",
  "password": "SecurePass123!"
}
```

**Response (200 OK):**
```json
{
  "user": {
    "id": "550e8400-e29b-41d4-a716-446655440000",
    "email": "john@example.com"
  },
  "session": {
    "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
    "refresh_token": "...",
    "expires_at": 1729000000
  }
}
```

#### Sign Out
```http
POST /api/auth/logout
```

**Response (200 OK):**
```json
{
  "success": true
}
```

#### Refresh Token
```http
POST /api/auth/refresh
```

**Request Body:**
```json
{
  "refresh_token": "..."
}
```

**Response (200 OK):**
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "refresh_token": "...",
  "expires_at": 1729000000
}
```

---

## Next.js API Routes

### User Profile

#### Get User Profile
```http
GET /api/profile
```

**Response (200 OK):**
```json
{
  "profile": {
    "id": "550e8400-e29b-41d4-a716-446655440000",
    "userId": "550e8400-e29b-41d4-a716-446655440000",
    "fullName": "John Doe",
    "phone": "+1-555-0123",
    "location": "San Francisco, CA",
    "linkedinUrl": "https://linkedin.com/in/johndoe",
    "githubUrl": "https://github.com/johndoe",
    "portfolioUrl": "https://johndoe.com",
    "targetRoles": ["Software Engineer", "Full Stack Developer"],
    "preferredLocations": ["Remote", "San Francisco"],
    "desiredSalaryMin": 120000,
    "desiredSalaryMax": 180000,
    "willingToRelocate": false,
    "summary": "Experienced software engineer with 5 years...",
    "skills": {
      "technical": ["Python", "React", "PostgreSQL"],
      "soft": ["Leadership", "Communication"]
    },
    "education": [
      {
        "degree": "B.S. Computer Science",
        "institution": "MIT",
        "graduationYear": 2018
      }
    ],
    "workExperience": [
      {
        "title": "Senior Software Engineer",
        "company": "Tech Corp",
        "startDate": "2020-01",
        "endDate": "2024-06",
        "description": "Led development of...",
        "achievements": [
          "Improved performance by 40%",
          "Mentored 3 junior developers"
        ]
      }
    ],
    "createdAt": "2024-10-01T10:00:00Z",
    "updatedAt": "2024-10-15T12:30:00Z"
  },
  "projects": [
    {
      "id": "...",
      "title": "E-commerce Platform",
      "description": "Built a full-stack e-commerce platform",
      "technologies": ["React", "Node.js", "PostgreSQL"],
      "role": "Lead Developer",
      "startDate": "2023-01",
      "endDate": "2023-12",
      "githubUrl": "https://github.com/johndoe/ecommerce",
      "demoUrl": "https://demo.example.com",
      "achievements": [
        "Handled 10K+ daily users",
        "99.9% uptime"
      ],
      "metrics": {
        "users": 10000,
        "performance_improvement": "40%"
      },
      "isFeatured": true,
      "relevanceTags": ["web", "backend", "database"]
    }
  ]
}
```

#### Update User Profile
```http
PUT /api/profile
```

**Request Body:**
```json
{
  "fullName": "John Doe",
  "location": "New York, NY",
  "targetRoles": ["Software Engineer", "Tech Lead"],
  "summary": "Updated professional summary..."
}
```

**Response (200 OK):**
```json
{
  "profile": {
    "id": "...",
    "fullName": "John Doe",
    "location": "New York, NY",
    "updatedAt": "2024-10-15T14:00:00Z"
  }
}
```

### Projects

#### List Projects
```http
GET /api/profile/projects
```

**Response (200 OK):**
```json
{
  "projects": [
    {
      "id": "...",
      "title": "E-commerce Platform",
      "description": "Built a full-stack e-commerce platform",
      "technologies": ["React", "Node.js"],
      "isFeatured": true
    }
  ]
}
```

#### Create Project
```http
POST /api/profile/projects
```

**Request Body:**
```json
{
  "title": "Mobile App",
  "description": "iOS and Android app for task management",
  "detailedDescription": "Full description for AI context...",
  "technologies": ["React Native", "Firebase"],
  "role": "Solo Developer",
  "startDate": "2024-01-01",
  "endDate": null,
  "githubUrl": "https://github.com/johndoe/mobile-app",
  "achievements": [
    "Published on App Store",
    "5K+ downloads"
  ],
  "isFeatured": false,
  "relevanceTags": ["mobile", "frontend"]
}
```

**Response (201 Created):**
```json
{
  "project": {
    "id": "...",
    "title": "Mobile App",
    "createdAt": "2024-10-15T14:30:00Z"
  }
}
```

#### Update Project
```http
PUT /api/profile/projects/:id
```

**Request Body:**
```json
{
  "title": "Updated Title",
  "isFeatured": true
}
```

**Response (200 OK):**
```json
{
  "project": {
    "id": "...",
    "title": "Updated Title",
    "updatedAt": "2024-10-15T15:00:00Z"
  }
}
```

#### Delete Project
```http
DELETE /api/profile/projects/:id
```

**Response (200 OK):**
```json
{
  "success": true
}
```

### Jobs

#### List Jobs
```http
GET /api/jobs?page=1&limit=20&source=linkedin&remote=true&minSalary=100000
```

**Query Parameters:**
- `page` (integer, default: 1) - Page number
- `limit` (integer, default: 20, max: 100) - Items per page
- `source` (string) - Filter by source: `linkedin`, `indeed`, `greenhouse`
- `remote` (boolean) - Filter remote jobs
- `minSalary` (integer) - Minimum salary
- `maxSalary` (integer) - Maximum salary
- `experienceLevel` (string) - `entry`, `mid`, `senior`, `lead`
- `sort` (string) - Sort by: `posted_date`, `relevance`, `salary`

**Response (200 OK):**
```json
{
  "jobs": [
    {
      "id": "...",
      "externalId": "linkedin_123456",
      "source": "linkedin",
      "sourceUrl": "https://linkedin.com/jobs/view/123456",
      "title": "Senior Software Engineer",
      "company": "Tech Corp",
      "companyLogoUrl": "https://...",
      "location": "San Francisco, CA",
      "remoteType": "hybrid",
      "description": "We are looking for...",
      "requirements": "5+ years of experience...",
      "responsibilities": "Design and develop...",
      "salaryMin": 150000,
      "salaryMax": 200000,
      "salaryCurrency": "USD",
      "employmentType": "full-time",
      "experienceLevel": "senior",
      "requiredSkills": ["Python", "React", "AWS"],
      "preferredSkills": ["Docker", "Kubernetes"],
      "benefits": ["Health Insurance", "401k", "Remote Work"],
      "postedDate": "2024-10-10T08:00:00Z",
      "scrapedAt": "2024-10-15T10:00:00Z",
      "expiresAt": "2024-11-10T08:00:00Z",
      "isActive": true,
      "relevanceScore": 0.87,
      "isFavorited": false
    }
  ],
  "pagination": {
    "page": 1,
    "limit": 20,
    "total": 150,
    "totalPages": 8,
    "hasMore": true
  }
}
```

#### Get Job Details
```http
GET /api/jobs/:id
```

**Response (200 OK):**
```json
{
  "job": {
    "id": "...",
    "title": "Senior Software Engineer",
    "company": "Tech Corp",
    "description": "We are looking for...",
    "parsedRequirements": {
      "years_experience": 5,
      "required_skills": ["Python", "React"],
      "nice_to_have": ["AWS", "Docker"],
      "education": "Bachelor's degree in CS or related field"
    },
    "relevanceScore": 0.87,
    "matchDetails": {
      "matching_skills": ["Python", "React", "PostgreSQL"],
      "missing_skills": ["AWS", "Docker"],
      "experience_match": true
    }
  }
}
```

#### Search Jobs
```http
POST /api/jobs/search
```

**Request Body:**
```json
{
  "query": "python developer",
  "filters": {
    "locations": ["Remote", "San Francisco"],
    "skills": ["Python", "Django"],
    "experienceLevel": ["mid", "senior"],
    "salaryMin": 120000,
    "remoteType": ["remote", "hybrid"]
  }
}
```

**Response (200 OK):**
```json
{
  "jobs": [...],
  "total": 45
}
```

#### Favorite Job
```http
POST /api/jobs/:id/favorite
```

**Response (200 OK):**
```json
{
  "success": true,
  "isFavorited": true
}
```

#### Hide Job
```http
POST /api/jobs/:id/hide
```

**Response (200 OK):**
```json
{
  "success": true,
  "isHidden": true
}
```

### Applications

#### List Applications
```http
GET /api/applications?status=applied&page=1&limit=20
```

**Query Parameters:**
- `status` (string) - Filter by status: `draft`, `applied`, `interviewing`, `offered`, `rejected`, `accepted`
- `page`, `limit` - Pagination

**Response (200 OK):**
```json
{
  "applications": [
    {
      "id": "...",
      "userId": "...",
      "job": {
        "id": "...",
        "title": "Senior Software Engineer",
        "company": "Tech Corp"
      },
      "status": "applied",
      "appliedAt": "2024-10-14T09:00:00Z",
      "cv": {
        "id": "...",
        "pdfUrl": "https://..."
      },
      "coverLetter": {
        "id": "...",
        "content": "Dear Hiring Manager..."
      },
      "notes": "Applied through LinkedIn Easy Apply",
      "followUpDate": "2024-10-21",
      "interviewDates": [
        {
          "type": "phone_screen",
          "date": "2024-10-18T14:00:00Z",
          "completed": false
        }
      ],
      "createdAt": "2024-10-14T08:00:00Z",
      "updatedAt": "2024-10-14T09:00:00Z"
    }
  ],
  "pagination": {...}
}
```

#### Create Application
```http
POST /api/applications
```

**Request Body:**
```json
{
  "jobId": "550e8400-e29b-41d4-a716-446655440000",
  "cvId": "550e8400-e29b-41d4-a716-446655440001",
  "coverLetterId": "550e8400-e29b-41d4-a716-446655440002",
  "notes": "Applied through company website",
  "status": "draft"
}
```

**Response (201 Created):**
```json
{
  "application": {
    "id": "...",
    "jobId": "...",
    "status": "draft",
    "createdAt": "2024-10-15T16:00:00Z"
  }
}
```

#### Update Application
```http
PUT /api/applications/:id
```

**Request Body:**
```json
{
  "status": "interviewing",
  "notes": "Had phone screen, technical interview scheduled",
  "interviewDates": [
    {
      "type": "technical",
      "date": "2024-10-22T10:00:00Z",
      "completed": false
    }
  ]
}
```

**Response (200 OK):**
```json
{
  "application": {
    "id": "...",
    "status": "interviewing",
    "updatedAt": "2024-10-15T16:30:00Z"
  }
}
```

#### Delete Application
```http
DELETE /api/applications/:id
```

**Response (200 OK):**
```json
{
  "success": true
}
```

### Generated CVs

#### List CVs
```http
GET /api/cvs?page=1&limit=20
```

**Response (200 OK):**
```json
{
  "cvs": [
    {
      "id": "...",
      "job": {
        "id": "...",
        "title": "Senior Software Engineer",
        "company": "Tech Corp"
      },
      "pdfUrl": "https://storage.app.com/cvs/...",
      "templateId": "...",
      "aiModel": "gpt-4o",
      "includedProjects": ["...", "..."],
      "highlightedSkills": ["Python", "React", "AWS"],
      "version": 1,
      "isLatest": true,
      "createdAt": "2024-10-15T10:00:00Z"
    }
  ],
  "pagination": {...}
}
```

#### Get CV Details
```http
GET /api/cvs/:id
```

**Response (200 OK):**
```json
{
  "cv": {
    "id": "...",
    "content": {
      "summary": "Experienced software engineer...",
      "experience": [...],
      "projects": [...],
      "skills": {...},
      "education": [...]
    },
    "htmlContent": "<html>...</html>",
    "pdfUrl": "https://...",
    "createdAt": "2024-10-15T10:00:00Z"
  }
}
```

#### Download CV
```http
GET /api/cvs/:id/download
```

**Response (200 OK):**
- Content-Type: `application/pdf`
- Returns PDF file

---

## FastAPI Routes

### Base URL: `http://localhost:8000` (dev) or `https://api.app.com` (prod)

### AI Generation

#### Generate CV
```http
POST /api/ai/cv/generate
```

**Request Body:**
```json
{
  "userId": "550e8400-e29b-41d4-a716-446655440000",
  "jobId": "550e8400-e29b-41d4-a716-446655440001",
  "templateId": "550e8400-e29b-41d4-a716-446655440002",
  "options": {
    "tone": "professional",
    "emphasizeSkills": ["Python", "React", "Leadership"],
    "includeProjects": ["proj-id-1", "proj-id-2"],
    "maxLength": 2000
  }
}
```

**Response (201 Created):**
```json
{
  "cvId": "...",
  "content": {
    "summary": "Results-driven software engineer...",
    "experience": [
      {
        "title": "Senior Software Engineer",
        "company": "Tech Corp",
        "startDate": "2020-01",
        "endDate": "2024-06",
        "highlights": [
          "Led development of microservices architecture serving 1M+ users",
          "Improved API response time by 40% through optimization",
          "Mentored team of 3 junior developers"
        ]
      }
    ],
    "projects": [
      {
        "title": "E-commerce Platform",
        "description": "Full-stack platform with React and Node.js",
        "highlights": [
          "Handled 10K+ daily active users",
          "Achieved 99.9% uptime"
        ],
        "technologies": ["React", "Node.js", "PostgreSQL"]
      }
    ],
    "skills": {
      "programming": ["Python", "JavaScript", "TypeScript"],
      "frameworks": ["React", "Django", "FastAPI"],
      "tools": ["Docker", "AWS", "PostgreSQL"]
    },
    "education": [
      {
        "degree": "B.S. Computer Science",
        "institution": "MIT",
        "graduationYear": 2018,
        "honors": "Magna Cum Laude"
      }
    ]
  },
  "pdfUrl": "https://storage.app.com/cvs/user-550e8400/cv-abc123.pdf",
  "generationTimeMs": 2300,
  "tokensUsed": {
    "input": 1500,
    "output": 800
  },
  "estimatedCost": 0.015
}
```

#### Generate Cover Letter
```http
POST /api/ai/cover-letter/generate
```

**Request Body:**
```json
{
  "userId": "550e8400-e29b-41d4-a716-446655440000",
  "jobId": "550e8400-e29b-41d4-a716-446655440001",
  "tone": "enthusiastic",
  "keyPoints": [
    "5 years of Python experience",
    "Led team of 3 developers",
    "Improved performance by 40%"
  ],
  "maxLength": 350
}
```

**Response (201 Created):**
```json
{
  "coverLetterId": "...",
  "content": "Dear Hiring Manager,\n\nI am writing to express my strong interest in the Senior Software Engineer position at Tech Corp...",
  "generationTimeMs": 1800,
  "tokensUsed": {
    "input": 1200,
    "output": 400
  },
  "estimatedCost": 0.008
}
```

#### Analyze CV Match
```http
POST /api/ai/cv/analyze
```

**Request Body:**
```json
{
  "cvContent": {
    "summary": "...",
    "experience": [...],
    "skills": [...]
  },
  "jobDescription": "We are seeking a Senior Software Engineer with 5+ years of experience in Python..."
}
```

**Response (200 OK):**
```json
{
  "matchScore": 0.85,
  "analysis": {
    "strengths": [
      "Strong Python background (5 years)",
      "Experience with React and modern frontend",
      "Leadership experience mentioned"
    ],
    "weaknesses": [
      "No AWS experience mentioned",
      "Docker not in skill list",
      "Limited DevOps background"
    ],
    "missingKeywords": [
      "AWS",
      "Docker",
      "Kubernetes",
      "CI/CD"
    ],
    "matchingKeywords": [
      "Python",
      "React",
      "PostgreSQL",
      "Leadership",
      "Microservices"
    ]
  },
  "suggestions": [
    "Add AWS projects if you have experience",
    "Highlight any Docker/containerization work",
    "Include specific metrics in achievements",
    "Add more details about team leadership",
    "Mention scalability challenges you've solved"
  ],
  "sectionScores": {
    "experience": 0.9,
    "skills": 0.75,
    "projects": 0.88,
    "education": 0.85
  }
}
```

### Job Scraping

#### Trigger Scraping Job
```http
POST /api/scraper/trigger
```

**Request Body:**
```json
{
  "userId": "550e8400-e29b-41d4-a716-446655440000",
  "sources": ["linkedin", "indeed", "greenhouse"],
  "preferences": {
    "roles": ["Software Engineer", "Full Stack Developer"],
    "locations": ["Remote", "San Francisco"],
    "experienceLevel": ["mid", "senior"],
    "minSalary": 120000
  },
  "maxResults": 100
}
```

**Response (202 Accepted):**
```json
{
  "jobId": "celery-task-abc123",
  "status": "queued",
  "estimatedDuration": 180
}
```

#### Check Scraping Status
```http
GET /api/scraper/status/:jobId
```

**Response (200 OK):**
```json
{
  "jobId": "celery-task-abc123",
  "status": "completed",
  "progress": {
    "totalSources": 3,
    "completedSources": 3,
    "jobsFound": 47,
    "jobsSaved": 35,
    "jobsSkipped": 12
  },
  "results": {
    "linkedin": {
      "found": 20,
      "saved": 15,
      "skipped": 5
    },
    "indeed": {
      "found": 15,
      "saved": 12,
      "skipped": 3
    },
    "greenhouse": {
      "found": 12,
      "saved": 8,
      "skipped": 4
    }
  },
  "startedAt": "2024-10-15T10:00:00Z",
  "completedAt": "2024-10-15T10:03:45Z",
  "durationSeconds": 225
}
```

### Document Parsing

#### Parse CV
```http
POST /api/parser/cv
Content-Type: multipart/form-data
```

**Request:**
```
file: [PDF or DOCX file]
```

**Response (200 OK):**
```json
{
  "parsedContent": {
    "name": "John Doe",
    "email": "john@example.com",
    "phone": "+1-555-0123",
    "location": "San Francisco, CA",
    "linkedinUrl": "https://linkedin.com/in/johndoe",
    "summary": "Experienced software engineer...",
    "experience": [
      {
        "title": "Senior Software Engineer",
        "company": "Tech Corp",
        "startDate": "2020-01",
        "endDate": "2024-06",
        "description": "Led development of..."
      }
    ],
    "skills": [
      "Python", "React", "PostgreSQL", "AWS"
    ],
    "education": [
      {
        "degree": "B.S. Computer Science",
        "institution": "MIT",
        "graduationYear": 2018
      }
    ],
    "projects": [
      {
        "title": "E-commerce Platform",
        "description": "Built full-stack application",
        "technologies": ["React", "Node.js"]
      }
    ]
  },
  "confidenceScore": 0.92,
  "warnings": [
    "Could not extract phone number with high confidence"
  ]
}
```

---

## Error Handling

### Error Response Format

All errors follow this standardized format:

```json
{
  "error": {
    "code": "ERROR_CODE",
    "message": "Human-readable error message",
    "details": {
      "field": "fieldName",
      "reason": "Additional context"
    }
  },
  "timestamp": "2024-10-15T10:00:00Z",
  "requestId": "req_abc123",
  "path": "/api/profile"
}
```

### HTTP Status Codes

| Code | Description | Usage |
|------|-------------|-------|
| **200** | OK | Successful GET, PUT, DELETE |
| **201** | Created | Successful POST (resource created) |
| **202** | Accepted | Async operation queued |
| **400** | Bad Request | Invalid input data |
| **401** | Unauthorized | Missing or invalid auth token |
| **403** | Forbidden | Insufficient permissions |
| **404** | Not Found | Resource doesn't exist |
| **409** | Conflict | Duplicate resource |
| **422** | Unprocessable Entity | Validation failed |
| **429** | Too Many Requests | Rate limit exceeded |
| **500** | Internal Server Error | Server error |
| **503** | Service Unavailable | Service temporarily down |

### Error Codes

#### Authentication Errors
- `AUTH_INVALID_CREDENTIALS` - Invalid email/password
- `AUTH_TOKEN_EXPIRED` - JWT token expired
- `AUTH_TOKEN_INVALID` - Invalid JWT token
- `AUTH_INSUFFICIENT_PERMISSIONS` - User lacks required permissions

#### Validation Errors
- `VALIDATION_FAILED` - Input validation failed
- `VALIDATION_REQUIRED_FIELD` - Required field missing
- `VALIDATION_INVALID_FORMAT` - Invalid field format
- `VALIDATION_OUT_OF_RANGE` - Value out of acceptable range

#### Resource Errors
- `RESOURCE_NOT_FOUND` - Requested resource doesn't exist
- `RESOURCE_ALREADY_EXISTS` - Duplicate resource
- `RESOURCE_DELETED` - Resource has been deleted

#### Rate Limiting
- `RATE_LIMIT_EXCEEDED` - Too many requests

#### External Service Errors
- `AI_SERVICE_ERROR` - AI provider error
- `AI_SERVICE_TIMEOUT` - AI generation timed out
- `SCRAPER_ERROR` - Job scraping failed
- `STORAGE_ERROR` - File storage error

### Example Error Responses

**400 Bad Request:**
```json
{
  "error": {
    "code": "VALIDATION_REQUIRED_FIELD",
    "message": "Job ID is required",
    "details": {
      "field": "jobId",
      "reason": "This field cannot be empty"
    }
  },
  "timestamp": "2024-10-15T10:00:00Z",
  "requestId": "req_abc123"
}
```

**401 Unauthorized:**
```json
{
  "error": {
    "code": "AUTH_TOKEN_EXPIRED",
    "message": "Your session has expired. Please log in again.",
    "details": {
      "expiredAt": "2024-10-15T09:00:00Z"
    }
  },
  "timestamp": "2024-10-15T10:00:00Z",
  "requestId": "req_abc123"
}
```

**429 Too Many Requests:**
```json
{
  "error": {
    "code": "RATE_LIMIT_EXCEEDED",
    "message": "Rate limit exceeded. Please try again later.",
    "details": {
      "limit": 10,
      "window": "1 minute",
      "retryAfter": 45
    }
  },
  "timestamp": "2024-10-15T10:00:00Z",
  "requestId": "req_abc123"
}
```

---

## Rate Limiting

### Rate Limits by Endpoint Category

| Category | Limit | Window | Applies To |
|----------|-------|--------|------------|
| **Authentication** | 5 requests | 5 minutes | `/api/auth/*` |
| **Read Operations** | 100 requests | 1 minute | GET endpoints |
| **Write Operations** | 30 requests | 1 minute | POST/PUT/DELETE endpoints |
| **AI Generation** | 10 requests | 1 minute | `/api/ai/*` |
| **Job Scraping** | 5 requests | 1 hour | `/api/scraper/trigger` |
| **File Upload** | 10 requests | 10 minutes | File upload endpoints |

### Rate Limit Headers

All responses include rate limit information:

```http
X-RateLimit-Limit: 100
X-RateLimit-Remaining: 95
X-RateLimit-Reset: 1729000000
```

### Exceeding Rate Limits

When rate limit is exceeded:
- HTTP 429 status code
- `Retry-After` header indicating seconds to wait
- Error response with details

---

## Webhooks

### Webhook Events

Configure webhooks to receive notifications about events:

#### Available Events

| Event | Description | Payload |
|-------|-------------|---------|
| `cv.generated` | CV generation completed | CV object |
| `cover_letter.generated` | Cover letter generated | Cover letter object |
| `job.scraped` | New jobs scraped | Jobs array |
| `application.status_changed` | Application status updated | Application object |

### Webhook Configuration

Configure webhooks in user settings:

```http
POST /api/webhooks
```

**Request:**
```json
{
  "url": "https://your-app.com/webhook",
  "events": ["cv.generated", "application.status_changed"],
  "secret": "whsec_your_secret"
}
```

### Webhook Payload Example

```json
{
  "event": "cv.generated",
  "timestamp": "2024-10-15T10:00:00Z",
  "data": {
    "cvId": "...",
    "userId": "...",
    "jobId": "...",
    "pdfUrl": "https://..."
  }
}
```

### Webhook Security

All webhooks include a signature header for verification:

```http
X-Webhook-Signature: sha256=abc123...
```

Verify using:
```python
import hmac
import hashlib

def verify_webhook(payload, signature, secret):
    computed = hmac.new(
        secret.encode(),
        payload.encode(),
        hashlib.sha256
    ).hexdigest()
    return hmac.compare_digest(f"sha256={computed}", signature)
```

---

## API Versioning

Current version: **v1**

Future versions will be accessible via:
```
/api/v2/...
```

Version 1 will be supported for at least 12 months after v2 release.

---

## SDK Examples

> **Note:** The SDK examples below are illustrative. You'll need to implement these client libraries or use standard HTTP clients like `fetch`, `axios`, or `requests`.

### JavaScript/TypeScript

```typescript
// Example using a hypothetical SDK (to be implemented)
import { JobAppClient } from '@job-app-ai/client';

const client = new JobAppClient({
  apiUrl: 'https://yourdomain.com/api',
  accessToken: 'your-jwt-token'
});

// Generate CV
const cv = await client.ai.generateCV({
  jobId: 'job-id',
  templateId: 'template-id',
  options: {
    tone: 'professional',
    emphasizeSkills: ['Python', 'React']
  }
});

// List jobs
const jobs = await client.jobs.list({
  page: 1,
  limit: 20,
  remote: true
});

// Create application
const application = await client.applications.create({
  jobId: 'job-id',
  cvId: cv.id,
  notes: 'Applied through company website'
});
```

### Python

```python
# Example using a hypothetical SDK (to be implemented)
from job_app_ai import JobAppClient

client = JobAppClient(
    api_url='https://yourdomain.com/api',
    access_token='your-jwt-token'
)

# Generate CV
cv = client.ai.generate_cv(
    job_id='job-id',
    template_id='template-id',
    options={
        'tone': 'professional',
        'emphasize_skills': ['Python', 'React']
    }
)

# List jobs
jobs = client.jobs.list(
    page=1,
    limit=20,
    remote=True
)

# Create application
application = client.applications.create(
    job_id='job-id',
    cv_id=cv.id,
    notes='Applied through company website'
)
```

---

## Testing

### Test Environment

**Local Testing:**
- Base URL: `http://localhost:8000`
- Create test accounts through the signup endpoint

**Staging Environment:**
- Configure your staging environment URL once deployed
- Set up test accounts specific to your deployment

### Postman Collection

You can create a Postman collection for easy API testing by exporting the OpenAPI/Swagger specification from FastAPI's auto-generated docs at `/docs` endpoint.

### Interactive API Docs

- **FastAPI Swagger UI:** `http://localhost:8000/docs`
- **FastAPI ReDoc:** `http://localhost:8000/redoc`

---

**Last Updated:** 2025-10-15
**Maintained By:** Engineering Team
