import { ReactNode } from 'react'

export function AuthLayout({
  title,
  subtitle,
  children,
}: {
  title: string
  subtitle: string
  children: ReactNode
}) {
  return (
    <div className="grid min-h-screen lg:grid-cols-2 bg-paper">
      {/* Left Column — Coffee-Tech style visual editorial hero panel */}
      <div className="relative hidden flex-col justify-between overflow-hidden bg-gradient-to-br from-[#0D0E13] via-[#12141C] to-[#181B26] px-16 py-16 text-ink lg:flex border-r border-mist-light/40">
        <div>
          <div className="flex items-center gap-3">
            <div className="flex h-9 w-9 items-center justify-center rounded-lg bg-gradient-to-br from-forest-500 to-forest-700 shadow-[0_0_15px_rgba(200,96,61,0.5)] border border-forest-300/40">
              <div className="flex flex-col gap-[3.5px] items-center">
                <span className="block h-[2.5px] w-4 rounded-full bg-ink" />
                <span className="block h-[2.5px] w-2.5 rounded-full bg-brass-300" />
                <span className="block h-[2.5px] w-4 rounded-full bg-forest-300" />
              </div>
            </div>
            <span className="font-display text-lg font-bold tracking-tight uppercase">
              COFFEE<span className="text-forest-500">TECH</span>
            </span>
          </div>
        </div>

        <div className="relative max-w-lg z-10">
          <div className="mb-4 inline-flex items-center gap-2 rounded-full border border-forest-500/30 bg-forest-500/10 px-3 py-1 text-xs font-mono font-semibold uppercase tracking-widest text-forest-500">
            <span className="h-1.5 w-1.5 rounded-full bg-forest-500 shadow-[0_0_8px_rgba(200,96,61,0.8)]" />
            ExpenseTrackerAI Platform
          </div>
          <h1 className="font-display text-5xl font-extrabold leading-[1.08] tracking-tight uppercase text-ink">
            See where your money goes, <span className="text-forest-500">before</span> it goes.
          </h1>
          <p className="mt-6 text-base leading-relaxed text-ink-soft">
            Automatic AI categorization, real-time budget telemetry, and financial analytics — precision engineered into your personal ledger.
          </p>
        </div>

        <div className="flex items-end justify-between text-xs font-mono uppercase tracking-widest text-mist">
          <span>© {new Date().getFullYear()} ExpenseTrackerAI</span>
          <span>Balance · Budgets · Insights</span>
        </div>

        {/* Ambient background glows */}
        <div
          className="pointer-events-none absolute -bottom-20 -left-20 h-96 w-96 rounded-full bg-forest-500/20 blur-[120px]"
          aria-hidden="true"
        />
        <div
          className="pointer-events-none absolute -right-20 top-1/4 h-80 w-80 rounded-full bg-brass-500/15 blur-[100px]"
          aria-hidden="true"
        />
      </div>

      {/* Right Column — Form card */}
      <div className="flex items-center justify-center bg-paper px-8 py-16">
        <div className="w-full max-w-md rounded-2xl border border-mist-light/60 bg-surface/90 p-8 md:p-10 shadow-[0_8px_32px_rgba(0,0,0,0.35)] backdrop-blur-md">
          <div className="mb-8 lg:hidden">
            <div className="flex items-center gap-3">
              <div className="flex h-9 w-9 items-center justify-center rounded-lg bg-gradient-to-br from-forest-500 to-forest-700">
                <div className="flex flex-col gap-[3.5px] items-center">
                  <span className="block h-[2.5px] w-4 rounded-full bg-ink" />
                  <span className="block h-[2.5px] w-2.5 rounded-full bg-brass-300" />
                </div>
              </div>
              <span className="font-display text-lg font-bold tracking-tight text-ink uppercase">
                COFFEE<span className="text-forest-500">TECH</span>
              </span>
            </div>
          </div>
          <h2 className="font-display text-2xl font-extrabold tracking-tight text-ink uppercase">{title}</h2>
          <p className="mt-2 text-sm text-ink-soft">{subtitle}</p>
          <div className="mt-8">{children}</div>
        </div>
      </div>
    </div>
  )
}
