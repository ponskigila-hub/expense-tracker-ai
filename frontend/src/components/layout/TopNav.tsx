import { useState, useRef, useEffect } from 'react'
import { NavLink, Link, useLocation } from 'react-router-dom'
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
  Info,
  ChevronDown,
  Wrench,
} from 'lucide-react'
import { useAuth } from '@/context/AuthContext'
import { useTheme } from '@/context/ThemeContext'

// Primary items visible directly in top bar
const mainNav = [
  { to: '/', label: 'Dashboard', icon: LayoutDashboard, end: true },
  { to: '/transactions', label: 'Transactions', icon: Receipt, end: false },
  { to: '/budgets', label: 'Budgets', icon: PiggyBank, end: false },
  { to: '/analytics', label: 'Analytics', icon: LineChart, end: false },
  { to: '/insights', label: 'AI Insights', icon: Sparkles, end: false },
]

// Secondary mini-features grouped under the adaptive "Tools" tab
const toolsNav = [
  { to: '/recurring', label: 'Recurring Payments', icon: Repeat, desc: 'Manage automated bill cycles', end: false },
  { to: '/receipts', label: 'OCR Scanner', icon: ScanLine, desc: 'Extract receipt data with AI', end: false },
  { to: '/export', label: 'Export Data', icon: Download, desc: 'Download CSV or JSON reports', end: false },
]

function BrandMark() {
  return (
    <div className="relative flex h-9 w-9 shrink-0 items-center justify-center rounded-xl bg-gradient-to-br from-forest-500 to-forest-700 shadow-[0_0_15px_rgba(195,65,30,0.4)] border border-forest-300/40">
      <div className="flex flex-col gap-[3px] items-center">
        <span className="block h-[2.5px] w-4.5 rounded-full bg-white" />
        <span className="block h-[2.5px] w-2.5 rounded-full bg-brass-300" />
        <span className="block h-[2.5px] w-4.5 rounded-full bg-forest-100" />
      </div>
    </div>
  )
}

export function TopNav() {
  const { user, logout } = useAuth()
  const { theme, toggleTheme } = useTheme()
  const location = useLocation()
  const [mobileOpen, setMobileOpen] = useState(false)
  const [toolsOpen, setToolsOpen] = useState(false)
  const dropdownRef = useRef<HTMLDivElement>(null)

  // Close dropdown on outside click or route change
  useEffect(() => {
    setToolsOpen(false)
    setMobileOpen(false)
  }, [location.pathname])

  useEffect(() => {
    function handleClickOutside(e: MouseEvent) {
      if (dropdownRef.current && !dropdownRef.current.contains(e.target as Node)) {
        setToolsOpen(false)
      }
    }
    document.addEventListener('mousedown', handleClickOutside)
    return () => document.removeEventListener('mousedown', handleClickOutside)
  }, [])

  const isToolsActive = toolsNav.some((t) => location.pathname === t.to)

  return (
    <header className="sticky top-0 z-40 border-b border-mist-light/70 bg-surface/95 dark:bg-[#0D0E13]/90 backdrop-blur-xl text-ink transition-all duration-300">
      <div className="mx-auto flex max-w-7xl items-center justify-between gap-4 px-4 md:px-8 py-2.5">
        {/* Brand LEDGER */}
        <Link to="/" className="flex shrink-0 items-center gap-3 group">
          <BrandMark />
          <span className="font-display text-2xl font-black tracking-tight text-ink uppercase group-hover:text-forest-500 transition-colors">
            LEDGER
          </span>
        </Link>

        {/* Adaptive Desktop Nav Bar — resized dynamically with 3 mini-features grouped under Tools */}
        <nav className="hidden items-center gap-1 xl:gap-2 lg:flex">
          {mainNav.map(({ to, label, icon: Icon, end }) => (
            <NavLink
              key={to}
              to={to}
              end={end}
              className={({ isActive }) =>
                clsx(
                  'flex shrink-0 items-center gap-1.5 rounded-lg px-3 py-2 text-xs font-bold uppercase tracking-wider transition-all duration-200',
                  isActive
                    ? 'bg-forest-500 text-white shadow-[0_0_14px_rgba(195,65,30,0.4)] border border-forest-300/40'
                    : 'text-ink-soft hover:bg-paper-dim hover:text-ink border border-transparent'
                )
              }
            >
              <Icon size={15} strokeWidth={2} />
              {label}
            </NavLink>
          ))}

          {/* Grouped Tools Dropdown */}
          <div className="relative" ref={dropdownRef}>
            <button
              onClick={() => setToolsOpen((o) => !o)}
              className={clsx(
                'flex items-center gap-1.5 rounded-lg px-3 py-2 text-xs font-bold uppercase tracking-wider transition-all duration-200 border',
                isToolsActive || toolsOpen
                  ? 'bg-forest-500/15 text-forest-500 border-forest-500/40 font-bold'
                  : 'text-ink-soft hover:bg-paper-dim hover:text-ink border-transparent'
              )}
            >
              <Wrench size={15} strokeWidth={2} />
              Tools
              <ChevronDown
                size={14}
                className={clsx('transition-transform duration-200', toolsOpen && 'rotate-180')}
              />
            </button>

            {toolsOpen && (
              <div className="absolute right-0 mt-2 w-64 rounded-xl border border-mist-light/70 bg-surface/98 dark:bg-[#12141C]/98 p-2 shadow-[0_12px_36px_rgba(0,0,0,0.25)] dark:shadow-[0_12px_36px_rgba(0,0,0,0.6)] backdrop-blur-xl z-50 animate-in fade-in slide-in-from-top-2 duration-150">
                <div className="px-3 py-1.5 text-[10px] font-mono font-bold uppercase tracking-widest text-mist border-b border-mist-light/40 mb-1">
                  Mini Features &amp; Utilities
                </div>
                {toolsNav.map(({ to, label, icon: Icon, desc }) => (
                  <NavLink
                    key={to}
                    to={to}
                    className={({ isActive }) =>
                      clsx(
                        'flex items-start gap-3 rounded-lg p-2.5 transition-colors',
                        isActive
                          ? 'bg-forest-500/20 text-forest-500'
                          : 'text-ink hover:bg-paper-dim'
                      )
                    }
                  >
                    <div className="p-1.5 rounded-md bg-forest-500/10 text-forest-500 shrink-0 mt-0.5">
                      <Icon size={16} />
                    </div>
                    <div>
                      <div className="text-xs font-bold uppercase tracking-wide leading-tight">{label}</div>
                      <div className="text-[11px] text-mist font-normal mt-0.5">{desc}</div>
                    </div>
                  </NavLink>
                ))}
              </div>
            )}
          </div>

          {/* About link */}
          <NavLink
            to="/about"
            className={({ isActive }) =>
              clsx(
                'flex shrink-0 items-center gap-1.5 rounded-lg px-3 py-2 text-xs font-bold uppercase tracking-wider transition-all duration-200',
                isActive
                  ? 'bg-forest-500 text-white shadow-[0_0_14px_rgba(195,65,30,0.4)] border border-forest-300/40'
                  : 'text-ink-soft hover:bg-paper-dim hover:text-ink border border-transparent'
              )
            }
          >
            <Info size={15} strokeWidth={2} />
            About
          </NavLink>
        </nav>

        {/* Right side user & theme controls */}
        <div className="flex shrink-0 items-center gap-3">
          <button
            onClick={toggleTheme}
            aria-label={theme === 'dark' ? 'Switch to light mode' : 'Switch to dark mode'}
            className="rounded-lg p-2 text-ink-soft transition-all duration-200 hover:bg-paper-dim hover:text-ink border border-mist-light/60"
          >
            {theme === 'dark' ? <Sun size={17} /> : <Moon size={17} />}
          </button>

          <div className="hidden items-center gap-3 pl-2 lg:flex border-l border-mist-light/60">
            <div className="flex items-center gap-2.5">
              <div className="flex h-8 w-8 items-center justify-center rounded-xl bg-forest-500 text-xs font-bold text-white shadow-[0_0_10px_rgba(195,65,30,0.3)]">
                {(user?.username || user?.email || '?').slice(0, 1).toUpperCase()}
              </div>
              <span className="text-xs font-bold text-ink leading-none">{user?.username || 'User'}</span>
            </div>
            <button
              onClick={logout}
              aria-label="Log out"
              title="Log Out"
              className="rounded-lg p-2 text-ink-soft transition-all duration-200 hover:bg-rust-500/20 hover:text-rust-500 border border-mist-light/60"
            >
              <LogOut size={16} />
            </button>
          </div>

          <button
            onClick={() => setMobileOpen((o) => !o)}
            aria-label={mobileOpen ? 'Close menu' : 'Open menu'}
            className="rounded-lg p-2 text-ink-soft hover:bg-paper-dim hover:text-ink lg:hidden border border-mist-light/60"
          >
            {mobileOpen ? <X size={20} /> : <Menu size={20} />}
          </button>
        </div>
      </div>

      {/* Mobile dropdown nav */}
      {mobileOpen && (
        <nav className="border-t border-mist-light/60 bg-paper/95 px-6 pb-6 pt-4 lg:hidden backdrop-blur-xl">
          <div className="space-y-1">
            {[...mainNav, ...toolsNav, { to: '/about', label: 'About', icon: Info, end: false }].map(
              ({ to, label, icon: Icon, end }) => (
                <NavLink
                  key={to}
                  to={to}
                  end={end}
                  onClick={() => setMobileOpen(false)}
                  className={({ isActive }) =>
                    clsx(
                      'flex items-center gap-3.5 rounded-lg px-4 py-2.5 text-xs font-bold uppercase tracking-wider transition-colors',
                      isActive
                        ? 'bg-forest-500 text-white shadow-[0_0_12px_rgba(195,65,30,0.4)]'
                        : 'text-ink-soft hover:bg-paper-dim hover:text-ink'
                    )
                  }
                >
                  <Icon size={17} strokeWidth={2} />
                  {label}
                </NavLink>
              )
            )}
          </div>
          <div className="mt-4 flex items-center justify-between border-t border-mist-light/60 px-2 pt-4">
            <div className="flex items-center gap-3">
              <div className="flex h-8 w-8 items-center justify-center rounded-xl bg-forest-500 text-xs font-bold text-white">
                {(user?.username || user?.email || '?').slice(0, 1).toUpperCase()}
              </div>
              <span className="truncate text-xs font-semibold text-ink">{user?.username}</span>
            </div>
            <button
              onClick={logout}
              className="flex items-center gap-2 rounded-lg bg-rust-500/20 px-3 py-1.5 text-xs font-bold uppercase tracking-wider text-rust-500 hover:bg-rust-500 hover:text-white transition-colors"
            >
              <LogOut size={15} /> Log out
            </button>
          </div>
        </nav>
      )}
    </header>
  )
}
