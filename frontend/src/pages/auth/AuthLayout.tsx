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
    <div className="grid min-h-screen lg:grid-cols-2">
      <div className="relative hidden flex-col justify-between overflow-hidden bg-forest-600 px-12 py-12 text-white lg:flex">
        <div>
          <div className="flex items-center gap-2.5">
            <div className="flex h-8 w-8 items-center justify-center rounded-md bg-forest-500">
              <div className="flex flex-col gap-[3px]">
                <span className="block h-[2px] w-4 rounded bg-paper" />
                <span className="block h-[2px] w-3 rounded bg-paper" />
                <span className="block h-[2px] w-4 rounded bg-brass-300" />
              </div>
            </div>
            <span className="font-display text-lg font-medium">Ledger</span>
          </div>
        </div>

        <div className="relative max-w-md">
          <p className="mb-4 text-xs font-semibold uppercase tracking-wider text-brass-300">
            ExpenseTrackerAI
          </p>
          <h1 className="font-display text-5xl font-medium leading-[1.1]">
            See where your money goes, <span className="text-brass-300">before</span> it goes.
          </h1>
          <p className="mt-5 text-forest-100/80">
            Automatic categorization, budget alerts, and spending insights —
            all in one ledger that stays honest with you.
          </p>
        </div>

        <div className="flex items-end justify-between text-sm text-forest-100/60">
          <span>© {new Date().getFullYear()} ExpenseTrackerAI</span>
          <span className="font-mono">balance · budgets · insights</span>
        </div>

        {/* Decorative ledger-tape lines */}
        <div
          className="pointer-events-none absolute -right-24 top-1/3 h-72 w-72 rounded-full bg-forest-500/40 blur-3xl"
          aria-hidden="true"
        />
      </div>

      <div className="flex items-center justify-center bg-paper px-6 py-12">
        <div className="w-full max-w-sm">
          <div className="mb-8 lg:hidden">
            <div className="flex items-center gap-2.5">
              <div className="flex h-8 w-8 items-center justify-center rounded-md bg-forest-500">
                <div className="flex flex-col gap-[3px]">
                  <span className="block h-[2px] w-4 rounded bg-paper" />
                  <span className="block h-[2px] w-3 rounded bg-paper" />
                  <span className="block h-[2px] w-4 rounded bg-brass-300" />
                </div>
              </div>
              <span className="font-display text-lg font-medium text-ink">Ledger</span>
            </div>
          </div>
          <h2 className="font-display text-2xl font-semibold tracking-tight text-ink">{title}</h2>
          <p className="mt-1.5 text-sm text-mist">{subtitle}</p>
          <div className="mt-8">{children}</div>
        </div>
      </div>
    </div>
  )
}
