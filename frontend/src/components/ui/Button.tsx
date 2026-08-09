import { ButtonHTMLAttributes, forwardRef } from 'react'
import clsx from 'clsx'

interface ButtonProps extends ButtonHTMLAttributes<HTMLButtonElement> {
  variant?: 'primary' | 'secondary' | 'ghost' | 'danger'
  size?: 'sm' | 'md'
}

const base =
  'inline-flex items-center justify-center gap-2 rounded font-medium transition-colors disabled:opacity-50 disabled:pointer-events-none'

const variants: Record<string, string> = {
  primary: 'bg-forest-500 text-white hover:bg-forest-600 active:bg-forest-700',
  secondary:
    'bg-surface text-ink border border-mist-light hover:border-forest-500 hover:text-forest-500',
  ghost: 'text-ink-soft hover:bg-paper-dim hover:text-ink',
  danger: 'bg-rust-500 text-white hover:bg-rust-600',
}

const sizes: Record<string, string> = {
  sm: 'h-8 px-3 text-sm',
  md: 'h-10 px-4 text-sm',
}

export const Button = forwardRef<HTMLButtonElement, ButtonProps>(
  ({ className, variant = 'primary', size = 'md', ...props }, ref) => (
    <button
      ref={ref}
      className={clsx(base, variants[variant], sizes[size], className)}
      {...props}
    />
  )
)
Button.displayName = 'Button'
