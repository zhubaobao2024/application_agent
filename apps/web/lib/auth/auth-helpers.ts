import { supabase } from './supabase'
import type { SignUpData, SignInData, User, Session } from '@/types/auth'

/**
 * Sign up a new user
 */
export async function signUp(data: SignUpData) {
  const { email, password, fullName } = data

  const { data: authData, error } = await supabase.auth.signUp({
    email,
    password,
    options: {
      data: {
        full_name: fullName,
      },
    },
  })

  if (error) {
    throw new Error(error.message)
  }

  return {
    user: authData.user ? mapUser(authData.user) : null,
    session: authData.session ? mapSession(authData.session) : null,
  }
}

/**
 * Sign in an existing user
 */
export async function signIn(data: SignInData) {
  const { email, password } = data

  const { data: authData, error } = await supabase.auth.signInWithPassword({
    email,
    password,
  })

  if (error) {
    throw new Error(error.message)
  }

  return {
    user: authData.user ? mapUser(authData.user) : null,
    session: authData.session ? mapSession(authData.session) : null,
  }
}

/**
 * Sign out the current user
 */
export async function signOut() {
  const { error } = await supabase.auth.signOut()

  if (error) {
    throw new Error(error.message)
  }
}

/**
 * Get the current session
 */
export async function getSession() {
  const { data, error } = await supabase.auth.getSession()

  if (error) {
    throw new Error(error.message)
  }

  return {
    user: data.session?.user ? mapUser(data.session.user) : null,
    session: data.session ? mapSession(data.session) : null,
  }
}

/**
 * Get the current user
 */
export async function getCurrentUser() {
  const { data, error } = await supabase.auth.getUser()

  if (error) {
    throw new Error(error.message)
  }

  return data.user ? mapUser(data.user) : null
}

/**
 * Refresh the current session
 */
export async function refreshSession() {
  const { data, error } = await supabase.auth.refreshSession()

  if (error) {
    throw new Error(error.message)
  }

  return {
    user: data.user ? mapUser(data.user) : null,
    session: data.session ? mapSession(data.session) : null,
  }
}

/**
 * Map Supabase user to our User type
 */
function mapUser(user: any): User {
  return {
    id: user.id,
    email: user.email!,
    emailConfirmed: user.email_confirmed_at ? true : false,
    createdAt: user.created_at,
  }
}

/**
 * Map Supabase session to our Session type
 */
function mapSession(session: any): Session {
  return {
    access_token: session.access_token,
    refresh_token: session.refresh_token,
    expires_at: session.expires_at,
    user: mapUser(session.user),
  }
}

/**
 * Listen to auth state changes
 */
export function onAuthStateChange(callback: (user: User | null) => void) {
  return supabase.auth.onAuthStateChange((_event, session) => {
    const user = session?.user ? mapUser(session.user) : null
    callback(user)
  })
}
