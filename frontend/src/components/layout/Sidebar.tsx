import { NavLink } from 'react-router-dom'
import clsx from 'clsx'
import {
  LayoutDashboard,
  Receipt,
  PiggyBank,
  LineChart,
  Repeat,
  ScanLine,
  Download,
  Sparkles,
  MessageCircle,
  LogOut,
} from 'lucide-react'
import { useAuth } from '@/context/AuthContext'

const nav = [
  { to: '/', label: 'Dashboard', icon: LayoutDashboard, end: true },
  { to: '/transactions', label: 'Transactions', icon: Receipt },
  { to: '/budgets', label: 'Budgets', icon: PiggyBank },
  { to: '/analytics', label: 'Analytics', icon: LineChart },
  { to: '/insights', label: 'AI Insights', icon: Sparkles },
  { to: '/assistant', label: 'AI Assistant', icon: MessageCircle },
  { to: '/recurring', label: 'Recurring', icon: Repeat },
  { to: '/receipts', label: 'Scan Receipt', icon: ScanLine },
  { to: '/export', label: 'Export', icon: Download },
]

export function Sidebar({ onNavigate }: { onNavigate?: () => void }) {
  const { user, logout } = useAuth()

  return (
    <div className="flex h-full flex-col bg-forest-600 text-white">
      <div className="flex items-center gap-2.5 px-5 pb-6 pt-6">
        <div className="flex h-8 w-8 items-center justify-center rounded-md bg-forest-500">
          <div className="flex flex-col gap-[3px]">
            <span className="block h-[2px] w-4 rounded bg-paper" />
            <span className="block h-[2px] w-3 rounded bg-paper" />
            <span className="block h-[2px] w-4 rounded bg-brass-300" />
          </div>
        </div>
        <div>
          <p className="font-display text-base font-medium leading-tight">Ledger</p>
          <p className="text-[11px] uppercase tracking-wider text-forest-100/70">ExpenseTrackerAI</p>
        </div>
      </div>

      <nav className="flex-1 space-y-0.5 px-3">
        {nav.map(({ to, label, icon: Icon, end }) => (
          <NavLink
            key={to}
            to={to}
            end={end}
            onClick={onNavigate}
            className={({ isActive }) =>
              clsx(
                'flex items-center gap-3 rounded-md px-3 py-2.5 text-2xl font-medium transition-colors',
                isActive
                  ? 'bg-forest-500 text-white'
                  : 'text-forest-100/80 hover:bg-forest-500/50 hover:text-white'
              )
            }
          >
            <Icon size={17} strokeWidth={2} />
            {label}
          </NavLink>
        ))}
      </nav>

      <div className="border-t border-forest-500/60 px-3 py-4">
        <div className="flex items-center gap-3 rounded-md px-3 py-2">
          <div className="flex h-8 w-8 items-center justify-center rounded-full bg-brass-500 text-sm font-semibold text-forest-700">
            {(user?.username || user?.email || '?').slice(0, 1).toUpperCase()}
          </div>
          <div className="min-w-0 flex-1">
            <p className="truncate text-sm font-medium text-white">{user?.username}</p>
            <p className="truncate text-xs text-forest-100/70">{user?.email}</p>
          </div>
          <button
            onClick={logout}
            aria-label="Log out"
            className="rounded p-1.5 text-forest-100/70 hover:bg-forest-500 hover:text-white"
          >
            <LogOut size={16} />
          </button>
        </div>
      </div>
    </div>
  )
}
