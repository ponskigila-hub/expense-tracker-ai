import { ReactNode } from 'react'
import clsx from 'clsx'
import { colorForCategory } from '@/lib/format'

export function CategoryBadge({ category }: { category: string }) {
  const color = colorForCategory(category)
  return (
    <span
      className="inline-flex items-center gap-1.5 rounded-full border px-2.5 py-0.5 text-xs font-medium capitalize"
      style={{
        color,
        borderColor: `${color}40`,
        backgroundColor: `${color}14`,
      }}
    >
      <span className="h-1.5 w-1.5 rounded-full" style={{ backgroundColor: color }} />
      {category}
    </span>
  )
}

export function TypeBadge({ type }: { type: 'income' | 'expense' }) {
  const isIncome = type === 'income'
  return (
    <span
      className={clsx(
        'inline-flex items-center rounded-full px-2.5 py-0.5 text-xs font-medium capitalize',
        isIncome ? 'bg-forest-50 text-forest-600' : 'bg-rust-100 text-rust-600'
      )}
    >
      {type}
    </span>
  )
}

export function ProgressBar({
  value,
  tone = 'forest',
}: {
  value: number
  tone?: 'forest' | 'brass' | 'rust'
}) {
  const clamped = Math.max(0, Math.min(100, value))
  const colors = {
    forest: 'bg-forest-500',
    brass: 'bg-brass-500',
    rust: 'bg-rust-500',
  }
  return (
    <div className="h-1.5 w-full overflow-hidden rounded-full bg-paper-dim">
      <div
        className={clsx('h-full rounded-full transition-all duration-500', colors[tone])}
        style={{ width: `${clamped}%` }}
      />
    </div>
  )
}

export function Spinner({ className }: { className?: string }) {
  return (
    <svg
      className={clsx('animate-spin', className)}
      viewBox="0 0 24 24"
      fill="none"
      aria-label="Loading"
    >
      <circle
        className="opacity-20"
        cx="12"
        cy="12"
        r="10"
        stroke="currentColor"
        strokeWidth="3"
      />
      <path
        d="M22 12a10 10 0 0 0-10-10"
        stroke="currentColor"
        strokeWidth="3"
        strokeLinecap="round"
      />
    </svg>
  )
}

export function EmptyState({
  icon,
  title,
  description,
  action,
}: {
  icon?: ReactNode
  title: string
  description?: string
  action?: ReactNode
}) {
  return (
    <div className="flex flex-col items-center justify-center gap-3 px-6 py-14 text-center">
      {icon && <div className="text-mist">{icon}</div>}
      <div>
        <p className="font-display text-lg font-medium tracking-tight text-ink">{title}</p>
        {description && <p className="mt-1 text-sm leading-relaxed text-mist">{description}</p>}
      </div>
      {action}
    </div>
  )
}

export function PageHeader({
  eyebrow,
  title,
  description,
  action,
}: {
  eyebrow?: string
  title: string
  description?: string
  action?: ReactNode
}) {
  return (
    <div className="mb-6 flex flex-wrap items-end justify-between gap-4">
      <div>
        {eyebrow && (
          <p className="mb-1.5 text-xs font-semibold uppercase tracking-[0.08em] text-forest-500">
            {eyebrow}
          </p>
        )}
        <h1 className="font-display text-[2rem] font-semibold leading-tight tracking-tight text-ink">
          {title}
        </h1>
        {description && <p className="mt-1.5 text-[0.9rem] leading-relaxed text-mist">{description}</p>}
      </div>
      {action}
    </div>
  )
}
