import { useEffect, useState } from 'react'
import { api } from '@/lib/api'
import type { CategorySummaryItem, MonthlySummaryItem, TrendPeriod, TrendPoint } from '@/types'
import { PageHeader, Spinner, EmptyState } from '@/components/ui/Misc'
import { Card, CardHeader } from '@/components/ui/Card'
import { TrendChart } from '@/components/charts/TrendChart'
import { CategoryDonut } from '@/components/charts/CategoryDonut'
import { MonthlyBarChart } from '@/components/charts/MonthlyBarChart'
import clsx from 'clsx'

const periods: { value: TrendPeriod; label: string }[] = [
  { value: '7d', label: '7 days' },
  { value: '30d', label: '30 days' },
  { value: '12m', label: '12 months' },
]

export default function Analytics() {
  const [period, setPeriod] = useState<TrendPeriod>('30d')
  const [trend, setTrend] = useState<TrendPoint[]>([])
  const [trendLoading, setTrendLoading] = useState(true)
  const [monthly, setMonthly] = useState<MonthlySummaryItem[]>([])
  const [categories, setCategories] = useState<CategorySummaryItem[]>([])
  const [initialLoading, setInitialLoading] = useState(true)

  // Refetches whenever the period toggle changes.
  useEffect(() => {
    setTrendLoading(true)
    api.analytics.trend(period).then((data) => {
      setTrend(data)
      setTrendLoading(false)
    })
  }, [period])

  // Runs once — monthly & category summaries don't depend on the period toggle.
  useEffect(() => {
    Promise.all([api.analytics.monthlySummary(), api.analytics.categorySummary()]).then(
      ([monthlyData, catData]) => {
        setMonthly(monthlyData)
        setCategories(catData)
        setInitialLoading(false)
      }
    )
  }, [])

  return (
    <div>
      <PageHeader eyebrow="Insights" title="Analytics" description="Understand your spending patterns over time." />

      <Card>
        <CardHeader
          title="Income vs. expenses"
          action={
            <div className="flex rounded-md border border-mist-light p-0.5">
              {periods.map((p) => (
                <button
                  key={p.value}
                  onClick={() => setPeriod(p.value)}
                  className={clsx(
                    'rounded px-3 py-1 text-xs font-medium transition-colors',
                    period === p.value ? 'bg-forest-500 text-white' : 'text-mist hover:text-ink'
                  )}
                >
                  {p.label}
                </button>
              ))}
            </div>
          }
        />
        <div className="px-3 pb-4 pt-2">
          {trendLoading ? (
            <div className="flex h-64 items-center justify-center"><Spinner className="h-5 w-5 text-forest-500" /></div>
          ) : trend.length ? (
            <TrendChart data={trend} />
          ) : (
            <EmptyState title="Not enough data yet" description="Trends appear once you log a few transactions." />
          )}
        </div>
      </Card>

      {initialLoading ? (
        <div className="mt-4 flex h-40 items-center justify-center"><Spinner className="h-5 w-5 text-forest-500" /></div>
      ) : (
        <div className="mt-4 grid gap-4 lg:grid-cols-5">
          <Card className="lg:col-span-3">
            <CardHeader title="Monthly summary" subtitle="Income and expenses by month" />
            <div className="px-3 pb-4 pt-2">
              {monthly.length ? (
                <MonthlyBarChart data={monthly} />
              ) : (
                <EmptyState title="No monthly data yet" description="Comes in once you've logged a full month." />
              )}
            </div>
          </Card>

          <Card className="lg:col-span-2">
            <CardHeader title="By category" subtitle="All-time breakdown" />
            <div className="p-5">
              <CategoryDonut data={categories} />
            </div>
          </Card>
        </div>
      )}
    </div>
  )
}
