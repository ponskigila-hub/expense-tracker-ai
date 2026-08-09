import { createContext, useContext, useEffect, useState, ReactNode, useCallback } from 'react'
import { api, getToken, setToken } from '@/lib/api'
import type { User } from '@/types'

interface AuthContextValue {
  user: User | null
  isAuthenticated: boolean
  isLoading: boolean
  login: (email: string, password: string) => Promise<void>
  register: (username: string, email: string, password: string) => Promise<void>
  logout: () => void
}

const AuthContext = createContext<AuthContextValue | undefined>(undefined)

const USER_KEY = 'ledger.user'

export function AuthProvider({ children }: { children: ReactNode }) {
  const [user, setUser] = useState<User | null>(null)
  const [isLoading, setIsLoading] = useState(true)

  useEffect(() => {
    const token = getToken()
    const storedUser = localStorage.getItem(USER_KEY)
    if (token && storedUser) {
      try {
        setUser(JSON.parse(storedUser))
      } catch {
        setUser(null)
      }
    }
    setIsLoading(false)
  }, [])

  const login = useCallback(async (email: string, password: string) => {
    const tokens = await api.auth.login({ email, password })
    setToken(tokens.access_token)
    // The API doesn't return the user on login, so we store what we
    // know locally (email) until a "me" endpoint exists.
    const fallbackUser: User = { id: 0, username: email.split('@')[0], email }
    localStorage.setItem(USER_KEY, JSON.stringify(fallbackUser))
    setUser(fallbackUser)
  }, [])

  const register = useCallback(async (username: string, email: string, password: string) => {
    const newUser = await api.auth.register({ username, email, password })
    localStorage.setItem(USER_KEY, JSON.stringify(newUser))
    await login(email, password)
  }, [login])

  const logout = useCallback(() => {
    setToken(null)
    localStorage.removeItem(USER_KEY)
    setUser(null)
  }, [])

  return (
    <AuthContext.Provider
      value={{ user, isAuthenticated: !!user, isLoading, login, register, logout }}
    >
      {children}
    </AuthContext.Provider>
  )
}

export function useAuth() {
  const ctx = useContext(AuthContext)
  if (!ctx) throw new Error('useAuth must be used within AuthProvider')
  return ctx
}
