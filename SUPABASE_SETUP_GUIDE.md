# Supabase Setup Guide

**Project:** AI Job Application Assistant
**Date:** 2025-10-15

---

## Table of Contents
1. [Create Supabase Account](#1-create-supabase-account)
2. [Create New Project](#2-create-new-project)
3. [Get API Keys](#3-get-api-keys)
4. [Configure Environment Variables](#4-configure-environment-variables)
5. [Set Up Database Schema](#5-set-up-database-schema)
6. [Configure Authentication](#6-configure-authentication)
7. [Test Connection](#7-test-connection)
8. [Optional: Set Up Storage](#8-optional-set-up-storage)

---

## 1. Create Supabase Account

### Step 1.1: Sign Up

1. Visit https://supabase.com
2. Click **"Start your project"** or **"Sign In"**
3. Sign up with one of these methods:
   - GitHub (Recommended for developers)
   - Email/Password
   - Google
   - GitLab

### Step 1.2: Verify Email

If you signed up with email:
1. Check your inbox for verification email
2. Click the verification link
3. You'll be redirected to Supabase dashboard

---

## 2. Create New Project

### Step 2.1: Create Organization (First Time Only)

1. If this is your first time, you'll be prompted to create an organization
2. Enter organization name: `Job App Assistant` (or your preferred name)
3. Click **"Create organization"**

### Step 2.2: Create Project

1. Click **"New Project"** button
2. Fill in project details:

```
Project Name: job-application-assistant
Database Password: [Generate a strong password - SAVE THIS!]
Region: Choose closest to you (e.g., "US West (N. California)")
Pricing Plan: Free (perfect for development)
```

3. Click **"Create new project"**
4. Wait 2-3 minutes for project to initialize

**⚠️ IMPORTANT:** Save your database password! You'll need it later.

---

## 3. Get API Keys

### Step 3.1: Navigate to API Settings

1. Once project is created, you'll see the dashboard
2. Click on **"Settings"** (gear icon) in the left sidebar
3. Click on **"API"** under Project Settings

### Step 3.2: Copy Your Keys

You'll see several keys. Copy these two:

**Project URL:**
```
https://your-project-id.supabase.co
```

**anon/public key:**
```
eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InlvdXItcHJvamVjdC1pZCIsInJvbGUiOiJhbm9uIiwiaWF0IjoxNjk...
```

**service_role key (Keep this secret!):**
```
eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InlvdXItcHJvamVjdC1pZCIsInJvbGUiOiJzZXJ2aWNlX3JvbGUiLCJpYXQiOjE2O...
```

### Step 3.3: Keep Keys Safe

**⚠️ SECURITY WARNING:**
- `anon` key is safe to use in frontend (it's public)
- `service_role` key should NEVER be exposed in frontend
- Never commit these keys to Git!

---

## 4. Configure Environment Variables

### Step 4.1: Create .env.local File

In your project root `apps/web/`, create `.env.local`:

```bash
cd apps/web
cp .env.example .env.local
```

### Step 4.2: Add Your Keys

Edit `apps/web/.env.local`:

```env
# Supabase Configuration
NEXT_PUBLIC_SUPABASE_URL=https://your-project-id.supabase.co
NEXT_PUBLIC_SUPABASE_ANON_KEY=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...

# API Configuration (for later phases)
NEXT_PUBLIC_API_URL=http://localhost:8000
```

Replace:
- `https://your-project-id.supabase.co` with your Project URL
- `eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...` with your anon key

### Step 4.3: Verify .gitignore

Make sure `.env.local` is in `.gitignore`:

```bash
# Check if it's ignored
cat apps/web/.gitignore | grep .env
```

Should show:
```
.env*.local
.env
```

---

## 5. Set Up Database Schema

### Step 5.1: Open SQL Editor

1. In Supabase dashboard, click **"SQL Editor"** in left sidebar
2. Click **"New query"**

### Step 5.2: Create user_profiles Table

Copy and paste this SQL, then click **"Run"**:

```sql
-- Enable UUID extension
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- Create user_profiles table
CREATE TABLE user_profiles (
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  user_id UUID REFERENCES auth.users(id) ON DELETE CASCADE UNIQUE NOT NULL,
  full_name VARCHAR(255) NOT NULL,
  phone VARCHAR(50),
  location VARCHAR(255),
  linkedin_url VARCHAR(500),
  github_url VARCHAR(500),
  portfolio_url VARCHAR(500),

  -- Preferences
  target_roles TEXT[],
  preferred_locations TEXT[],
  desired_salary_min INTEGER,
  desired_salary_max INTEGER,
  willing_to_relocate BOOLEAN DEFAULT false,

  -- Base CV content
  summary TEXT,
  skills JSONB,
  education JSONB,
  work_experience JSONB,

  created_at TIMESTAMPTZ DEFAULT NOW(),
  updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- Create index
CREATE INDEX idx_user_profiles_user_id ON user_profiles(user_id);

-- Enable Row Level Security
ALTER TABLE user_profiles ENABLE ROW LEVEL SECURITY;

-- Create policies
CREATE POLICY "Users can view own profile"
  ON user_profiles FOR SELECT
  USING (auth.uid() = user_id);

CREATE POLICY "Users can insert own profile"
  ON user_profiles FOR INSERT
  WITH CHECK (auth.uid() = user_id);

CREATE POLICY "Users can update own profile"
  ON user_profiles FOR UPDATE
  USING (auth.uid() = user_id);

-- Add updated_at trigger
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
  NEW.updated_at = NOW();
  RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER update_user_profiles_updated_at
  BEFORE UPDATE ON user_profiles
  FOR EACH ROW
  EXECUTE FUNCTION update_updated_at_column();
```

✅ You should see "Success. No rows returned"

### Step 5.3: Create projects Table

Run this query:

```sql
-- Create projects table
CREATE TABLE projects (
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  user_id UUID REFERENCES auth.users(id) ON DELETE CASCADE NOT NULL,

  title VARCHAR(255) NOT NULL,
  description TEXT,
  detailed_description TEXT,
  technologies TEXT[],

  role VARCHAR(100),
  start_date DATE,
  end_date DATE,

  github_url VARCHAR(500),
  demo_url VARCHAR(500),

  achievements TEXT[],
  metrics JSONB,

  is_featured BOOLEAN DEFAULT false,
  relevance_tags TEXT[],

  created_at TIMESTAMPTZ DEFAULT NOW(),
  updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- Create indexes
CREATE INDEX idx_projects_user_id ON projects(user_id);
CREATE INDEX idx_projects_tags ON projects USING GIN(relevance_tags);

-- Enable RLS
ALTER TABLE projects ENABLE ROW LEVEL SECURITY;

-- Create policies
CREATE POLICY "Users can view own projects"
  ON projects FOR SELECT
  USING (auth.uid() = user_id);

CREATE POLICY "Users can insert own projects"
  ON projects FOR INSERT
  WITH CHECK (auth.uid() = user_id);

CREATE POLICY "Users can update own projects"
  ON projects FOR UPDATE
  USING (auth.uid() = user_id);

CREATE POLICY "Users can delete own projects"
  ON projects FOR DELETE
  USING (auth.uid() = user_id);

-- Add updated_at trigger
CREATE TRIGGER update_projects_updated_at
  BEFORE UPDATE ON projects
  FOR EACH ROW
  EXECUTE FUNCTION update_updated_at_column();
```

✅ Success!

### Step 5.4: Verify Tables

1. Click **"Table Editor"** in left sidebar
2. You should see:
   - `user_profiles` table
   - `projects` table
   - `auth.users` table (created by Supabase)

---

## 6. Configure Authentication

### Step 6.1: Enable Email Auth

1. Click **"Authentication"** in left sidebar
2. Click **"Providers"**
3. Make sure **"Email"** is enabled (should be by default)

### Step 6.2: Configure Email Settings (Optional)

For development, you can use Supabase's built-in email service:

1. Go to **Authentication** → **Email Templates**
2. You can customize:
   - Confirmation email
   - Magic link email
   - Password recovery email

**For Production:** You'll want to set up custom SMTP (Gmail, SendGrid, etc.)

### Step 6.3: Disable Email Confirmation (Development Only)

For faster development, you can disable email confirmation:

1. Go to **Authentication** → **Providers**
2. Click on **"Email"**
3. **Uncheck** "Enable email confirmations"
4. Click **"Save"**

**⚠️ NOTE:** Re-enable this for production!

### Step 6.4: Configure Site URL

1. Go to **Authentication** → **URL Configuration**
2. Set **Site URL**: `http://localhost:3000`
3. Add **Redirect URLs**:
   - `http://localhost:3000`
   - `http://localhost:3000/dashboard`
4. Click **"Save"**

---

## 7. Test Connection

### Step 7.1: Start Your Dev Server

```bash
# From project root
pnpm dev

# Server should start at http://localhost:3000
```

### Step 7.2: Test Signup

1. Go to http://localhost:3000
2. Click **"Get Started"**
3. Fill in signup form:
   ```
   Full Name: Test User
   Email: test@example.com
   Password: Test1234!
   Confirm Password: Test1234!
   ```
4. Click **"Create account"**
5. You should be redirected to `/dashboard`

### Step 7.3: Verify in Supabase

1. Go to Supabase dashboard
2. Click **"Authentication"** → **"Users"**
3. You should see your test user!

### Step 7.4: Test Login

1. Click **"Sign Out"** in dashboard
2. Click **"Sign In"**
3. Enter credentials
4. Should redirect back to dashboard

### Step 7.5: Check Database

1. Go to **"Table Editor"**
2. Select `auth.users` table
3. You should see your user record

---

## 8. Optional: Set Up Storage

For CV PDFs and other files (Phase 5):

### Step 8.1: Create Storage Bucket

1. Click **"Storage"** in left sidebar
2. Click **"New bucket"**
3. Enter:
   ```
   Name: cvs
   Public: No (keep private)
   ```
4. Click **"Create bucket"**

### Step 8.2: Set Storage Policies

Click on `cvs` bucket → **"Policies"** → **"New policy"**

**Read Policy:**
```sql
-- Users can read own CVs
((bucket_id = 'cvs'::text) AND (auth.uid() = (storage.foldername(name))[1]::uuid))
```

**Insert Policy:**
```sql
-- Users can upload own CVs
((bucket_id = 'cvs'::text) AND (auth.uid() = (storage.foldername(name))[1]::uuid))
```

---

## 9. Troubleshooting

### Issue: "Invalid API key"

**Solution:**
- Double-check your `.env.local` file
- Make sure you copied the full key (they're very long!)
- Restart dev server after updating `.env.local`

### Issue: "User already registered"

**Solution:**
1. Go to Supabase → Authentication → Users
2. Find the user
3. Delete the user
4. Try signup again

### Issue: "Failed to fetch"

**Solution:**
- Check your internet connection
- Verify Project URL is correct
- Check Supabase project status (should be "Active")

### Issue: Can't see tables in Table Editor

**Solution:**
- Make sure SQL queries ran successfully
- Refresh the page
- Check SQL Editor for error messages

### Issue: Login works but redirects fail

**Solution:**
- Check redirect URLs in Authentication → URL Configuration
- Make sure `http://localhost:3000` is listed

---

## 10. Next Steps

Now that Supabase is set up:

✅ **Completed:**
- Supabase project created
- API keys configured
- Database tables created
- Authentication working
- RLS policies set up

🚀 **Ready for:**
- Phase 3: User Profile Management
- Creating profile edit forms
- Adding projects management
- Building the full application

---

## 11. Useful Supabase Features

### Database Explorer
- View all tables and data
- Run SQL queries
- Create indexes and functions

### Authentication
- Manage users
- View sessions
- Configure providers (Google, GitHub, etc.)

### SQL Editor
- Write and execute SQL
- Save queries as snippets
- View query history

### API Docs
- Auto-generated REST API docs
- Auto-generated TypeScript types
- GraphQL support

### Logs
- View real-time logs
- Debug authentication issues
- Monitor API usage

---

## 12. Production Checklist

Before deploying to production:

- [ ] Enable email confirmation
- [ ] Set up custom SMTP
- [ ] Configure production Site URL
- [ ] Set up database backups
- [ ] Enable 2FA for Supabase account
- [ ] Review RLS policies
- [ ] Set up monitoring/alerts
- [ ] Configure rate limiting
- [ ] Update CORS settings
- [ ] Review security settings

---

## 13. Resources

### Documentation
- [Supabase Docs](https://supabase.com/docs)
- [Supabase Auth Guide](https://supabase.com/docs/guides/auth)
- [Row Level Security](https://supabase.com/docs/guides/auth/row-level-security)
- [Supabase CLI](https://supabase.com/docs/guides/cli)

### Tutorials
- [Next.js + Supabase Auth](https://supabase.com/docs/guides/auth/auth-helpers/nextjs)
- [Database Design](https://supabase.com/docs/guides/database/tables)
- [Storage](https://supabase.com/docs/guides/storage)

### Community
- [Discord](https://discord.supabase.com/)
- [GitHub Discussions](https://github.com/supabase/supabase/discussions)
- [Twitter](https://twitter.com/supabase)

---

## 14. Quick Reference

### Environment Variables Template

```env
# apps/web/.env.local

# Supabase (Required)
NEXT_PUBLIC_SUPABASE_URL=https://your-project-id.supabase.co
NEXT_PUBLIC_SUPABASE_ANON_KEY=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...

# Backend API (For later)
NEXT_PUBLIC_API_URL=http://localhost:8000
```

### Testing Credentials

For development testing:
```
Email: test@example.com
Password: Test1234!
```

### Useful SQL Queries

**View all users:**
```sql
SELECT * FROM auth.users;
```

**View user profiles:**
```sql
SELECT * FROM user_profiles;
```

**Delete test user:**
```sql
DELETE FROM auth.users WHERE email = 'test@example.com';
```

**Reset database (DANGER!):**
```sql
TRUNCATE user_profiles CASCADE;
TRUNCATE projects CASCADE;
```

---

**Setup Status:** Ready for development
**Last Updated:** 2025-10-15
**Estimated Setup Time:** 10-15 minutes
