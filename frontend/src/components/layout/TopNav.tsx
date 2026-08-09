import { useState } from 'react'
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
  LogOut,
  Menu,
  X,
  Sun,
  Moon,
} from 'lucide-react'
import { useAuth } from '@/context/AuthContext'
import { useTheme } from '@/context/ThemeContext'

const nav = [
  { to: '/', label: 'Dashboard', icon: LayoutDashboard, end: true },
  { to: '/transactions', label: 'Transactions', icon: Receipt },
  { to: '/budgets', label: 'Budgets', icon: PiggyBank },
  { to: '/analytics', label: 'Analytics', icon: LineChart },
  { to: '/insights', label: 'Insights', icon: Sparkles },
  { to: '/recurring', label: 'Recurring', icon: Repeat },
  { to: '/receipts', label: 'Scan', icon: ScanLine },
  { to: '/export', label: 'Export', icon: Download },
]

function BrandMark() {
  return (
    <div className="flex h-8 w-8 shrink-0 items-center justify-center rounded-md bg-forest-500">
      <div className="flex flex-col gap-[3px]">
        <span className="block h-[2px] w-4 rounded bg-paper" />
        <span className="block h-[2px] w-3 rounded bg-paper" />
        <span className="block h-[2px] w-4 rounded bg-brass-300" />
      </div>
    </div>
  )
}

export function TopNav() {
  const { user, logout } = useAuth()
  const { theme, toggleTheme } = useTheme()
  const [mobileOpen, setMobileOpen] = useState(false)

  return (
    <header className="sticky top-0 z-30 border-b border-forest-500/40 bg-forest-600 text-white">
      <div className="mx-auto flex max-w-6xl items-center gap-3 px-4 md:px-8">
        {/* Brand */}
        <div className="flex shrink-0 items-center gap-2.5 py-3">
          <BrandMark />
          <span className="hidden font-display text-base font-medium leading-none tracking-tight sm:block">
            Ledger
          </span>
        </div>

        {/* Desktop nav — horizontal, scrolls if the viewport is tight
            rather than wrapping, so the bar always stays one row. */}
        <nav className="hidden flex-1 items-center gap-1 overflow-x-auto py-2 scrollbar-thin lg:flex">
          {nav.map(({ to, label, icon: Icon, end }) => (
            <NavLink
              key={to}
              to={to}
              end={end}
              className={({ isActive }) =>
                clsx(
                  'flex shrink-0 items-center gap-1.5 whitespace-nowrap rounded-md px-3 py-2 text-sm font-medium transition-colors',
                  isActive
                    ? 'bg-forest-500 text-white'
                    : 'text-forest-100/80 hover:bg-forest-500/50 hover:text-white'
                )
              }
            >
              <Icon size={16} strokeWidth={2} />
              {label}
            </NavLink>
          ))}
        </nav>

        {/* Right side controls */}
        <div className="ml-auto flex shrink-0 items-center gap-1 py-2">
          <button
            onClick={toggleTheme}
            aria-label={theme === 'dark' ? 'Switch to light mode' : 'Switch to dark mode'}
            className="rounded-md p-2 text-forest-100/80 transition-colors hover:bg-forest-500 hover:text-white"
          >
            {theme === 'dark' ? <Sun size={17} /> : <Moon size={17} />}
          </button>

          <div className="hidden items-center gap-2 pl-1 lg:flex">
            <div className="flex h-8 w-8 items-center justify-center rounded-full bg-brass-500 text-sm font-semibold text-forest-700">
              {(user?.username || user?.email || '?').slice(0, 1).toUpperCase()}
            </div>
            <button
              onClick={logout}
              aria-label="Log out"
              className="rounded-md p-2 text-forest-100/80 transition-colors hover:bg-forest-500 hover:text-white"
            >
              <LogOut size={17} />
            </button>
          </div>

          <button
            onClick={() => setMobileOpen((o) => !o)}
            aria-label={mobileOpen ? 'Close menu' : 'Open menu'}
            className="rounded-md p-2 text-forest-100/80 hover:bg-forest-500 hover:text-white lg:hidden"
          >
            {mobileOpen ? <X size={20} /> : <Menu size={20} />}
          </button>
        </div>
      </div>

      {/* Mobile dropdown nav */}
      {mobileOpen && (
        <nav className="border-t border-forest-500/40 px-4 pb-3 pt-1 lg:hidden">
          {nav.map(({ to, label, icon: Icon, end }) => (
            <NavLink
              key={to}
              to={to}
              end={end}
              onClick={() => setMobileOpen(false)}
              className={({ isActive }) =>
                clsx(
                  'flex items-center gap-3 rounded-md px-3 py-2.5 text-sm font-medium transition-colors',
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
          <div className="mt-2 flex items-center justify-between border-t border-forest-500/40 px-3 pt-3">
            <div className="flex items-center gap-2">
              <div className="flex h-7 w-7 items-center justify-center rounded-full bg-brass-500 text-xs font-semibold text-forest-700">
                {(user?.username || user?.email || '?').slice(0, 1).toUpperCase()}
              </div>
              <span className="truncate text-sm text-forest-100/80">{user?.username}</span>
            </div>
            <button
              onClick={logout}
              className="flex items-center gap-1.5 rounded-md px-2 py-1.5 text-sm font-medium text-forest-100/80 hover:bg-forest-500/50 hover:text-white"
            >
              <LogOut size={15} /> Log out
            </button>
          </div>
        </nav>
      )}
    </header>
  )
}
