import clsx from 'clsx'
import { splitMoney } from '@/lib/format'

interface MoneyDisplayProps {
  amount: number
  size?: 'hero' | 'lg' | 'md' | 'sm'
  tone?: 'ink' | 'forest' | 'rust' | 'brass' | 'auto'
  showSign?: boolean
  className?: string
}

const sizeMap = {
  hero: { whole: 'text-5xl md:text-6xl', cents: 'text-xl md:text-2xl' },
  lg: { whole: 'text-[1.75rem]', cents: 'text-base' },
  md: { whole: 'text-xl', cents: 'text-sm' },
  sm: { whole: 'text-sm', cents: 'text-[11px]' },
}

const toneMap = {
  ink: 'text-ink',
  forest: 'text-forest-500',
  rust: 'text-rust-500',
  brass: 'text-brass-600',
  auto: '',
}

/**
 * The app's signature typographic motif: the whole-dollar amount is set in
 * Fraunces (display serif) while the cents ride along in IBM Plex Mono at a
 * muted weight — like a ledger total with its fine print. Used everywhere a
 * monetary figure needs to read as the headline of its card.
 */
export function MoneyDisplay({
  amount,
  size = 'md',
  tone = 'ink',
  showSign = false,
  className,
}: MoneyDisplayProps) {
  const { whole, cents, negative } = splitMoney(amount)
  const resolvedTone = tone === 'auto' ? (negative ? 'rust' : 'forest') : tone
  const sign = negative ? '−' : showSign ? '+' : ''

  return (
    <span
      className={clsx('inline-flex items-baseline font-display tabular', toneMap[resolvedTone], className)}
    >
      <span className={clsx(sizeMap[size].whole, 'font-medium leading-none tracking-tight')}>
        {sign}${whole}
      </span>
      <span className={clsx(sizeMap[size].cents, 'ml-0.5 font-mono font-normal leading-none opacity-60')}>
        .{cents}
      </span>
    </span>
  )
}
