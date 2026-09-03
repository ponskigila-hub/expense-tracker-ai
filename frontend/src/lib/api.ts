import type {
  AuthTokens,
  Budget,
  BudgetInput,
  CategorySummaryItem,
  ChatMessage,
  ChatResponse,
  DashboardSummary,
  InsightResponse,
  MonthlySummaryItem,
  PaginatedTransactions,
  ReceiptScanResult,
  RecurringTransaction,
  RecurringTransactionInput,
  Transaction,
  TransactionFilters,
  TransactionInput,
  TrendPeriod,
  TrendPoint,
  User,
} from '@/types'

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000'

const TOKEN_KEY = 'ledger.access_token'

export function getToken(): string | null {
  return localStorage.getItem(TOKEN_KEY)
}

export function setToken(token: string | null) {
  if (token) localStorage.setItem(TOKEN_KEY, token)
  else localStorage.removeItem(TOKEN_KEY)
}

export class ApiError extends Error {
  status: number
  constructor(message: string, status: number) {
    super(message)
    this.status = status
  }
}

async function request<T>(
  path: string,
  options: RequestInit = {}
): Promise<T> {
  const token = getToken()
  const headers: Record<string, string> = {
    ...(options.body && !(options.body instanceof FormData)
      ? { 'Content-Type': 'application/json' }
      : {}),
    ...(token ? { Authorization: `Bearer ${token}` } : {}),
    ...((options.headers as Record<string, string>) || {}),
  }

  const res = await fetch(`${API_BASE_URL}${path}`, { ...options, headers })

  if (res.status === 204) return undefined as T

  const isJson = res.headers.get('content-type')?.includes('application/json')
  const data = isJson ? await res.json().catch(() => null) : null

  if (!res.ok) {
    const message =
      (data && (data.detail || data.message)) ||
      `Request failed with status ${res.status}`
    const text =
      typeof message === 'string' ? message : JSON.stringify(message)
    throw new ApiError(text, res.status)
  }

  return data as T
}

async function requestBlob(path: string, options: RequestInit = {}): Promise<Blob> {
  const token = getToken()
  const res = await fetch(`${API_BASE_URL}${path}`, {
    ...options,
    headers: {
      ...(token ? { Authorization: `Bearer ${token}` } : {}),
      ...((options.headers as Record<string, string>) || {}),
    },
  })
  if (!res.ok) {
    throw new ApiError(`Export failed with status ${res.status}`, res.status)
  }
  return res.blob()
}

function qs(params: object): string {
  const search = new URLSearchParams()
  Object.entries(params as Record<string, unknown>).forEach(([key, value]) => {
    if (value !== undefined && value !== null && value !== '') {
      search.set(key, String(value))
    }
  })
  const s = search.toString()
  return s ? `?${s}` : ''
}

export const api = {
  auth: {
    register: (data: { username: string; email: string; password: string }) =>
      request<User>('/register', { method: 'POST', body: JSON.stringify(data) }),
    login: (data: { email: string; password: string }) =>
      request<AuthTokens>('/login', { method: 'POST', body: JSON.stringify(data) }),
  },

  transactions: {
    list: (filters: TransactionFilters = {}) =>
      request<PaginatedTransactions>(`/transactions${qs(filters)}`),
    get: (id: number) => request<Transaction>(`/transactions/${id}`),
    create: (data: TransactionInput) =>
      request<Transaction>('/transactions', {
        method: 'POST',
        body: JSON.stringify(data),
      }),
    update: (id: number, data: TransactionInput) =>
      request<Transaction>(`/transactions/${id}`, {
        method: 'PUT',
        body: JSON.stringify(data),
      }),
    remove: (id: number) =>
      request<{ message?: string }>(`/transactions/${id}`, { method: 'DELETE' }),
  },

  budgets: {
    list: () => request<Budget[]>('/budget'),
    create: (data: BudgetInput) =>
      request<Budget>('/budget', { method: 'POST', body: JSON.stringify(data) }),
    update: (id: number, data: { amount: number }) =>
      request<Budget>(`/budget/${id}`, { method: 'PUT', body: JSON.stringify(data) }),
    remove: (id: number) => request<void>(`/budget/${id}`, { method: 'DELETE' }),
  },

  analytics: {
    dashboard: () => request<DashboardSummary>('/dashboard'),
    monthlySummary: () => request<MonthlySummaryItem[]>('/summary/monthly'),
    categorySummary: () => request<CategorySummaryItem[]>('/summary/category'),
    trend: (period: TrendPeriod = '30d') =>
      request<TrendPoint[]>(`/summary/trend${qs({ period })}`),
  },

  insights: {
    get: () => request<InsightResponse>('/insights'),
  },

  assistant: {
    ask: (message: string, history: ChatMessage[] = []) =>
      request<ChatResponse>('/chat', {
        method: 'POST',
        body: JSON.stringify({ message, history }),
      }),
  },

  prediction: {
    predictCategory: (description: string) =>
      request<{ description: string; category: string; confidence: number; method: string }>(
        '/predict-category',
        { method: 'POST', body: JSON.stringify({ description }) }
      ),
  },

  receipts: {
    scan: (file: File, autoSave: boolean) => {
      const form = new FormData()
      form.append('file', file)
      return request<ReceiptScanResult>(
        `/receipts/scan${qs({ auto_save: autoSave })}`,
        { method: 'POST', body: form }
      )
    },
  },

  recurring: {
    list: () => request<RecurringTransaction[]>('/recurring-transactions'),
    create: (data: RecurringTransactionInput) =>
      request<RecurringTransaction>('/recurring-transactions', {
        method: 'POST',
        body: JSON.stringify(data),
      }),
    update: (id: number, data: Partial<RecurringTransactionInput> & { is_active?: boolean }) =>
      request<RecurringTransaction>(`/recurring-transactions/${id}`, {
        method: 'PUT',
        body: JSON.stringify(data),
      }),
    remove: (id: number) =>
      request<void>(`/recurring-transactions/${id}`, { method: 'DELETE' }),
    runNow: () =>
      request<Transaction[]>('/recurring-transactions/run', { method: 'POST' }),
  },

  export: {
    download: async (
      format: 'csv' | 'excel' | 'pdf',
      range: { date_from?: string; date_to?: string } = {}
    ) => {
      const blob = await requestBlob(`/export/${format}${qs(range)}`)
      const ext = format === 'excel' ? 'xlsx' : format
      const url = URL.createObjectURL(blob)
      const a = document.createElement('a')
      a.href = url
      a.download = `transactions.${ext}`
      document.body.appendChild(a)
      a.click()
      a.remove()
      URL.revokeObjectURL(url)
    },
  },
}
