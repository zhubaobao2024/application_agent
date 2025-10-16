# AI Job Application Assistant - Frontend

Next.js 14 frontend application for the AI Job Application Assistant platform.

## Tech Stack

- **Framework**: Next.js 14 (App Router)
- **Language**: TypeScript
- **Styling**: Tailwind CSS
- **UI Components**: shadcn/ui (Radix UI)
- **State Management**: Zustand + TanStack Query
- **Forms**: React Hook Form + Zod
- **API Client**: Axios
- **Authentication**: Supabase

## Getting Started

### Prerequisites

- Node.js 18+
- pnpm 8+

### Installation

```bash
# Install dependencies (from project root)
pnpm install

# Or specifically for web app
pnpm --filter web install
```

### Environment Variables

Copy `.env.example` to `.env.local` and fill in your values:

```bash
cp .env.example .env.local
```

Required variables:
- `NEXT_PUBLIC_SUPABASE_URL` - Your Supabase project URL
- `NEXT_PUBLIC_SUPABASE_ANON_KEY` - Your Supabase anonymous key
- `NEXT_PUBLIC_API_URL` - Backend API URL (default: http://localhost:8000)

### Development

```bash
# Start development server (from project root)
pnpm dev

# Or from this directory
pnpm dev
```

Open [http://localhost:3000](http://localhost:3000) in your browser.

### Build

```bash
pnpm build
```

### Lint

```bash
pnpm lint
```

### Type Check

```bash
pnpm type-check
```

## Project Structure

```
apps/web/
├── app/                    # Next.js App Router
│   ├── (auth)/            # Auth pages (login, signup)
│   ├── (dashboard)/       # Dashboard pages
│   ├── layout.tsx         # Root layout
│   ├── page.tsx           # Landing page
│   └── globals.css        # Global styles
├── components/
│   ├── ui/                # shadcn/ui components
│   ├── layout/            # Layout components
│   └── shared/            # Shared components
├── lib/
│   ├── api/               # API client functions
│   ├── auth/              # Auth helpers
│   ├── validations/       # Zod schemas
│   └── utils.ts           # Utility functions
├── stores/                # Zustand stores
├── hooks/                 # Custom React hooks
├── types/                 # TypeScript types
└── public/                # Static assets
```

## Adding shadcn/ui Components

```bash
# Add a component (e.g., button)
pnpm dlx shadcn-ui@latest add button

# Add multiple components
pnpm dlx shadcn-ui@latest add button input card
```

## Available Scripts

- `pnpm dev` - Start development server
- `pnpm build` - Build for production
- `pnpm start` - Start production server
- `pnpm lint` - Run ESLint
- `pnpm type-check` - Run TypeScript type checking

## Development Guidelines

### Code Style

- Use functional components with hooks
- Follow TypeScript best practices
- Use Tailwind CSS for styling
- Keep components small and focused
- Write clear, descriptive variable names

### Component Structure

```tsx
// Good component structure
import { ComponentProps } from '@/types/component'

interface Props {
  title: string
  description?: string
}

export function Component({ title, description }: Props) {
  return (
    <div className="space-y-4">
      <h2 className="text-2xl font-bold">{title}</h2>
      {description && <p>{description}</p>}
    </div>
  )
}
```

### API Integration

```tsx
// Use custom hooks for API calls
import { useJobs } from '@/hooks/useJobs'

export function JobList() {
  const { data, isLoading, error } = useJobs()

  if (isLoading) return <LoadingSpinner />
  if (error) return <ErrorState error={error} />

  return <JobGrid jobs={data} />
}
```

### Form Handling

```tsx
// Use React Hook Form + Zod
import { useForm } from 'react-hook-form'
import { zodResolver } from '@hookform/resolvers/zod'
import { loginSchema } from '@/lib/validations/auth'

export function LoginForm() {
  const form = useForm({
    resolver: zodResolver(loginSchema),
  })

  const onSubmit = (data) => {
    // Handle form submission
  }

  return <form onSubmit={form.handleSubmit(onSubmit)}>...</form>
}
```

## Learn More

- [Next.js Documentation](https://nextjs.org/docs)
- [Tailwind CSS](https://tailwindcss.com/docs)
- [shadcn/ui](https://ui.shadcn.com)
- [TanStack Query](https://tanstack.com/query/latest)
- [Zustand](https://zustand-demo.pmnd.rs/)
