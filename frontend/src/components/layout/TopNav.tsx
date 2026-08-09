import { useState } from 'react'
import { NavLink, Link } from 'react-router-dom'
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
  ChevronDown,
  ShieldCheck,
  Cpu,
} from 'lucide-react'
import { useAuth } from '@/context/AuthContext'
import { useTheme } from '@/context/ThemeContext'

const mainNav = [
  { to: '/', label: 'Dashboard', icon: LayoutDashboard, end: true },
  { to: '/transactions', label: 'Transactions', icon: Receipt, end: false },
  { to: '/budgets', label: 'Budgets', icon: PiggyBank, end: false },
  { to: '/analytics', label: 'Analytics', icon: LineChart, end: false },
  { to: '/insights', label: 'AI Insights', icon: Sparkles, end: false },
]

const secondaryNav = [
  { to: '/recurring', label: 'Recurring', icon: Repeat, end: false },
  { to: '/receipts', label: 'OCR Scanner', icon: ScanLine, end: false },
  { to: '/export', label: 'Export Data', icon: Download, end: false },
]

function BrandMark() {
  return (
    <div className="relative flex h-10 w-10 shrink-0 items-center justify-center rounded-xl bg-gradient-to-br from-forest-500 via-forest-600 to-forest-700 shadow-[0_0_20px_rgba(200,96,61,0.5)] border border-forest-300/40 transition-transform duration-300 hover:scale-105">
      <div className="flex flex-col gap-[3.5px] items-center">
        <span className="block h-[2.5px] w-5 rounded-full bg-ink" />
        <span className="block h-[2.5px] w-3 rounded-full bg-brass-300" />
        <span className="block h-[2.5px] w-5 rounded-full bg-forest-300" />
      </div>
      <span className="absolute -bottom-0.5 -right-0.5 h-2.5 w-2.5 rounded-full bg-emerald-400 border-2 border-[#0D0E13] shadow-[0_0_8px_rgba(52,211,153,0.8)]" />
    </div>
  )
}

export function TopNav() {
  const { user, logout } = useAuth()
  const { theme, toggleTheme } = useTheme()
  const [mobileOpen, setMobileOpen] = useState(false)
  const [toolsOpen, setToolsOpen] = useState(false)

  return (
    <header className="sticky top-0 z-40 border-b border-mist-light/50 bg-[#0D0E13]/90 backdrop-blur-xl text-ink transition-all duration-300">
      {/* Top marquee status bar inspired by Coffee-Tech */}
      <div className="hidden border-b border-mist-light/30 bg-[#0A0B0F] px-8 py-1.5 text-[11px] font-mono uppercase tracking-widest text-mist md:flex items-center justify-between">
        <div className="flex items-center gap-6">
          <span className="flex items-center gap-2 text-forest-500 font-semibold">
            <Cpu size={13} /> AI Engine: Active
          </span>
          <span className="text-mist-light">|</span>
          <span>System Status: 99.98% Telemetry Stream</span>
        </div>
        <div className="flex items-center gap-6">
          <span className="flex items-center gap-1.5 text-emerald-400">
            <ShieldCheck size={13} /> End-to-End Encrypted
          </span>
          <span className="text-mist-light">|</span>
          <span className="text-ink-soft">Session: {user?.username || user?.email}</span>
        </div>
      </div>

      <div className="mx-auto flex max-w-7xl items-center justify-between gap-4 px-4 md:px-8">
        {/* Brand */}
        <Link to="/" className="flex shrink-0 items-center gap-3.5 py-3.5 group">
          <BrandMark />
          <div className="flex flex-col">
            <span className="font-display text-xl font-black tracking-tight text-ink uppercase group-hover:text-forest-300 transition-colors">
              COFFEE<span className="text-forest-500">TECH</span>
            </span>
            <span className="text-[9.5px] font-mono tracking-[0.22em] text-mist uppercase leading-none font-semibold">
              ExpenseTrackerAI
            </span>
          </div>
        </Link>

        {/* Desktop nav — refined editorial layout */}
        <nav className="hidden items-center gap-1.5 lg:flex">
          {mainNav.map(({ to, label, icon: Icon, end }) => (
            <NavLink
              key={to}
              to={to}
              end={end}
              className={({ isActive }) =>
                clsx(
                  'flex shrink-0 items-center gap-2 rounded-lg px-3.5 py-2 text-xs font-bold uppercase tracking-wider transition-all duration-200',
                  isActive
                    ? 'bg-forest-500 text-white shadow-[0_0_16px_rgba(200,96,61,0.5)] border border-forest-300/40'
                    : 'text-ink-soft hover:bg-surface hover:text-ink border border-transparent'
                )
              }
            >
              <Icon size={15} strokeWidth={2} />
              {label}
            </NavLink>
          ))}

          {/* Tools dropdown */}
          <div className="relative ml-1">
            <button
              onClick={() => setToolsOpen((o) => !o)}
              className={clsx(
                'flex items-center gap-1.5 rounded-lg px-3.5 py-2 text-xs font-bold uppercase tracking-wider text-ink-soft hover:bg-surface hover:text-ink border border-transparent transition-all duration-200',
                toolsOpen && 'bg-surface text-ink'
              )}
            >
              Tools &amp; Utilites
              <ChevronDown size={14} className={clsx('transition-transform duration-200', toolsOpen && 'rotate-180')} />
            </button>

            {toolsOpen && (
              <div
                className="absolute right-0 mt-2 w-52 rounded-xl border border-mist-light/60 bg-surface/95 p-2 shadow-[0_12px_36px_rgba(0,0,0,0.5)] backdrop-blur-xl z-50 animate-in fade-in slide-in-from-top-2 duration-200"
                onMouseLeave={() => setToolsOpen(false)}
              >
                {secondaryNav.map(({ to, label, icon: Icon }) => (
                  <NavLink
                    key={to}
                    to={to}
                    onClick={() => setToolsOpen(false)}
                    className={({ isActive }) =>
                      clsx(
                        'flex items-center gap-3 rounded-lg px-3 py-2.5 text-xs font-semibold uppercase tracking-wider transition-colors',
                        isActive
                          ? 'bg-forest-500/20 text-forest-300 font-bold'
                          : 'text-ink-soft hover:bg-paper-dim hover:text-ink'
                      )
                    }
                  >
                    <Icon size={16} className="text-forest-500" />
                    {label}
                  </NavLink>
                ))}
              </div>
            )}
          </div>
        </nav>

        {/* Right side controls */}
        <div className="flex shrink-0 items-center gap-3 py-3">
          <button
            onClick={toggleTheme}
            aria-label={theme === 'dark' ? 'Switch to light mode' : 'Switch to dark mode'}
            className="rounded-lg p-2.5 text-ink-soft transition-all duration-200 hover:bg-surface hover:text-ink border border-mist-light/50 hover:border-forest-500/50"
          >
            {theme === 'dark' ? <Sun size={17} /> : <Moon size={17} />}
          </button>

          <div className="hidden items-center gap-3 pl-2 lg:flex border-l border-mist-light/40">
            <div className="flex items-center gap-2.5">
              <div className="flex h-9 w-9 items-center justify-center rounded-xl bg-gradient-to-br from-forest-500 to-brass-500 text-xs font-bold text-white shadow-[0_0_12px_rgba(200,96,61,0.4)] border border-forest-300/30">
                {(user?.username || user?.email || '?').slice(0, 1).toUpperCase()}
              </div>
              <div className="flex flex-col">
                <span className="text-xs font-bold text-ink leading-none">{user?.username || 'User'}</span>
                <span className="text-[10px] font-mono text-mist">Logged In</span>
              </div>
            </div>
            <button
              onClick={logout}
              aria-label="Log out"
              title="Log Out"
              className="ml-2 rounded-lg p-2.5 text-ink-soft transition-all duration-200 hover:bg-rust-500/20 hover:text-rust-500 border border-mist-light/50"
            >
              <LogOut size={17} />
            </button>
          </div>

          <button
            onClick={() => setMobileOpen((o) => !o)}
            aria-label={mobileOpen ? 'Close menu' : 'Open menu'}
            className="rounded-lg p-2 text-ink-soft hover:bg-surface hover:text-ink lg:hidden border border-mist-light/50"
          >
            {mobileOpen ? <X size={22} /> : <Menu size={22} />}
          </button>
        </div>
      </div>

      {/* Mobile dropdown nav */}
      {mobileOpen && (
        <nav className="border-t border-mist-light/50 bg-paper-dim/95 px-6 pb-6 pt-4 lg:hidden backdrop-blur-xl">
          <div className="space-y-1">
            {[...mainNav, ...secondaryNav].map(({ to, label, icon: Icon, end }) => (
              <NavLink
                key={to}
                to={to}
                end={end}
                onClick={() => setMobileOpen(false)}
                className={({ isActive }) =>
                  clsx(
                    'flex items-center gap-3.5 rounded-lg px-4 py-3 text-xs font-bold uppercase tracking-wider transition-colors',
                    isActive
                      ? 'bg-forest-500 text-white shadow-[0_0_12px_rgba(200,96,61,0.5)]'
                      : 'text-ink-soft hover:bg-surface hover:text-ink'
                  )
                }
              >
                <Icon size={18} strokeWidth={2} />
                {label}
              </NavLink>
            ))}
          </div>
          <div className="mt-4 flex items-center justify-between border-t border-mist-light/50 px-2 pt-4">
            <div className="flex items-center gap-3">
              <div className="flex h-8 w-8 items-center justify-center rounded-xl bg-brass-500 text-xs font-bold text-white">
                {(user?.username || user?.email || '?').slice(0, 1).toUpperCase()}
              </div>
              <span className="truncate text-xs font-semibold text-ink">{user?.username}</span>
            </div>
            <button
              onClick={logout}
              className="flex items-center gap-2 rounded-lg bg-rust-500/20 px-3 py-2 text-xs font-bold uppercase tracking-wider text-rust-500 hover:bg-rust-500 hover:text-white transition-colors"
            >
              <LogOut size={15} /> Log out
            </button>
          </div>
        </nav>
      )}
    </header>
  )
}
