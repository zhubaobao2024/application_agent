export interface User {
  id: string
  email: string
  emailConfirmed?: boolean
  createdAt?: string
}

export interface Session {
  access_token: string
  refresh_token: string
  expires_at: number
  user: User
}

export interface AuthResponse {
  user: User
  session: Session
}

export interface SignUpData {
  email: string
  password: string
  fullName: string
}

export interface SignInData {
  email: string
  password: string
}
