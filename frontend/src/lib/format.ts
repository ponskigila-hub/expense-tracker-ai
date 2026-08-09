export function splitMoney(amount: number): { whole: string; cents: string; negative: boolean } {
  const negative = amount < 0
  const abs = Math.abs(amount)
  const fixed = abs.toFixed(2)
  const [whole, cents] = fixed.split('.')
  const withThousands = whole.replace(/\B(?=(\d{3})+(?!\d))/g, ',')
  return { whole: withThousands, cents, negative }
}

export function formatMoney(amount: number): string {
  const { whole, cents, negative } = splitMoney(amount)
  return `${negative ? '-' : ''}$${whole}.${cents}`
}

export function formatDate(dateStr: string): string {
  const d = new Date(dateStr + (dateStr.length === 10 ? 'T00:00:00' : ''))
  return d.toLocaleDateString('en-US', { month: 'short', day: 'numeric', year: 'numeric' })
}

export function formatDateShort(dateStr: string): string {
  const d = new Date(dateStr + (dateStr.length === 10 ? 'T00:00:00' : ''))
  return d.toLocaleDateString('en-US', { month: 'short', day: 'numeric' })
}

export function formatMonthLabel(month: string): string {
  // "2026-07" -> "Jul 2026"
  const [y, m] = month.split('-')
  const d = new Date(Number(y), Number(m) - 1, 1)
  return d.toLocaleDateString('en-US', { month: 'short', year: 'numeric' })
}

export function todayISO(): string {
  return new Date().toISOString().slice(0, 10)
}

// Matches the labels the backend's ML category classifier was trained on
// (see backend/app/ml/training_data.py), plus "Other" as a manual fallback.
export const CATEGORIES = [
  'Food',
  'Groceries',
  'Transportation',
  'Bills',
  'Entertainment',
  'Shopping',
  'Health',
  'Education',
  'Subscription',
  'Travel',
  'Income',
  'Other',
] as const

export const CATEGORY_COLORS: Record<string, string> = {
  food: '#B98527',
  groceries: '#5C9382',
  transport: '#3D6E8F',
  transportation: '#3D6E8F',
  housing: '#7A5C9E',
  rent: '#7A5C9E',
  utilities: '#4C7A9E',
  bills: '#4C7A9E',
  subscription: '#8B6FB0',
  entertainment: '#C0637A',
  shopping: '#CB8B76',
  health: '#3F9E7A',
  healthcare: '#3F9E7A',
  education: '#7093C2',
  travel: '#5AA6A0',
  salary: '#1F5C4C',
  income: '#1F5C4C',
  other: '#8B948E',
  others: '#8B948E',
  miscellaneous: '#8B948E',
}

export function colorForCategory(category: string): string {
  const key = category.trim().toLowerCase()
  return CATEGORY_COLORS[key] || '#7A8380'
}
