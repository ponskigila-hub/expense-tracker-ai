export type TransactionType = 'income' | 'expense'

export interface Transaction {
  id: number
  date: string // YYYY-MM-DD
  description: string
  amount: number
  type: TransactionType
  category: string
  notes: string | null
  user_id: number
  created_at: string
}

export interface TransactionInput {
  date: string
  description: string
  amount: number
  type: TransactionType
  category: string
  notes?: string | null
}

export interface PaginatedTransactions {
  items: Transaction[]
  total: number
  page: number
  page_size: number
  total_pages: number
}

export interface TransactionFilters {
  category?: string
  type?: TransactionType
  date_from?: string
  date_to?: string
  min_amount?: number
  max_amount?: number
  search?: string
  sort_by?: 'date' | 'amount' | 'description' | 'category' | 'created_at'
  sort_order?: 'asc' | 'desc'
  page?: number
  page_size?: number
}

export interface Budget {
  id: number
  category: string
  amount: number
  spent: number
  remaining: number
  percentage_used: number
  is_exceeded: boolean
  warning: string | null
  updated_at: string
}

export interface BudgetInput {
  category: string
  amount: number
}

export interface DashboardSummary {
  balance: number
  income: number
  expense: number
}

export interface MonthlySummaryItem {
  month: string
  income: number
  expense: number
  balance: number
}

export interface CategorySummaryItem {
  category: string
  total: number
  percentage: number
}

export interface TrendPoint {
  label: string
  income: number
  expense: number
}

export type TrendPeriod = '7d' | '30d' | '12m'

export interface InsightResponse {
  insights: string[]
  generated_by: 'llm' | 'rule_based'
}

export interface RecurringTransaction {
  id: number
  description: string
  amount: number
  type: TransactionType
  category: string
  notes: string | null
  day_of_month: number
  is_active: boolean
  last_run_date: string | null
  created_at: string
}

export interface RecurringTransactionInput {
  description: string
  amount: number
  type: TransactionType
  category: string
  notes?: string | null
  day_of_month: number
}

export interface ReceiptScanResult {
  receipt_id: number
  merchant: string | null
  date: string | null
  amount: number | null
  category: string | null
  category_confidence: number | null
  raw_text: string
  saved: boolean
  transaction: Transaction | null
}

export interface User {
  id: number
  username: string
  email: string
}

export interface AuthTokens {
  access_token: string
  token_type: string
}
