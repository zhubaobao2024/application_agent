'use client'

import { useEffect } from 'react'
import { useAuthStore } from '@/stores/authStore'
import { getSession, onAuthStateChange } from '@/lib/auth/auth-helpers'

export function AuthProvider({ children }: { children: React.ReactNode }) {
  const setSession = useAuthStore((state) => state.setSession)
  const setUser = useAuthStore((state) => state.setUser)
  const setLoading = useAuthStore((state) => state.setLoading)

  useEffect(() => {
    // Check for existing session on mount
    getSession()
      .then(({ session }) => {
        setSession(session)
      })
      .catch((error) => {
        console.error('Error getting session:', error)
      })
      .finally(() => {
        setLoading(false)
      })

    // Listen for auth state changes
    const { data: authListener } = onAuthStateChange((user) => {
      setUser(user)
      setLoading(false)
    })

    // Cleanup listener on unmount
    return () => {
      authListener?.subscription?.unsubscribe()
    }
  }, [setSession, setUser, setLoading])

  return <>{children}</>
}
