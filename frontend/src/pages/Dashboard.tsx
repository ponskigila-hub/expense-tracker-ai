import { useEffect, useState } from 'react'
import { Link } from 'react-router-dom'
import { ArrowUpRight, ArrowDownRight, Wallet, Sparkles, Plus } from 'lucide-react'
import { api } from '@/lib/api'
import type { CategorySummaryItem, DashboardSummary, Transaction, TrendPoint } from '@/types'
import { Card, CardHeader } from '@/components/ui/Card'
import { MoneyDisplay } from '@/components/ui/MoneyDisplay'
import { PageHeader, Spinner, TypeBadge, CategoryBadge, EmptyState } from '@/components/ui/Misc'
import { Button } from '@/components/ui/Button'
import { TrendChart } from '@/components/charts/TrendChart'
import { CategoryDonut } from '@/components/charts/CategoryDonut'
import { formatDateShort, formatMoney } from '@/lib/format'
import { Receipt } from 'lucide-react'
import { TransactionFormModal } from '@/pages/transactions/TransactionFormModal'

export default function Dashboard() {
  const [summary, setSummary] = useState<DashboardSummary | null>(null)
  const [trend, setTrend] = useState<TrendPoint[]>([])
  const [categories, setCategories] = useState<CategorySummaryItem[]>([])
  const [recent, setRecent] = useState<Transaction[]>([])
  const [insight, setInsight] = useState<string | null>(null)
  const [loading, setLoading] = useState(true)
  const [addOpen, setAddOpen] = useState(false)

  async function loadAll() {
    setLoading(true)
    const [dash, trendData, catData, txns, insights] = await Promise.allSettled([
      api.analytics.dashboard(),
      api.analytics.trend('30d'),
      api.analytics.categorySummary(),
      api.transactions.list({ page: 1, page_size: 5, sort_by: 'date', sort_order: 'desc' }),
      api.insights.get(),
    ])
    if (dash.status === 'fulfilled') setSummary(dash.value)
    if (trendData.status === 'fulfilled') setTrend(trendData.value)
    if (catData.status === 'fulfilled') setCategories(catData.value)
    if (txns.status === 'fulfilled') setRecent(txns.value.items)
    if (insights.status === 'fulfilled' && insights.value.insights.length > 0) {
      setInsight(insights.value.insights[0])
    }
    setLoading(false)
  }

  useEffect(() => {
    loadAll()
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [])

  if (loading) {
    return (
      <div className="flex h-96 items-center justify-center">
        <Spinner className="h-6 w-6 text-forest-500" />
      </div>
    )
  }

  return (
    <div>
      <PageHeader
        eyebrow="Overview"
        title="Dashboard"
        description="Your finances at a glance."
        action={
          <Button onClick={() => setAddOpen(true)}>
            <Plus size={16} /> Add transaction
          </Button>
        }
      />

      {/* Hero balance + stat cards */}
      <div className="grid gap-4 lg:grid-cols-3">
        <Card className="lg:col-span-1 flex flex-col justify-between p-6">
          <div className="flex items-center gap-2 text-sm font-medium text-mist">
            <Wallet size={16} />
            Current balance
          </div>
          <div className="mt-4">
            <MoneyDisplay amount={summary?.balance ?? 0} size="hero" tone="auto" />
          </div>
          <p className="mt-3 text-sm text-mist">Income minus expenses, all time.</p>
        </Card>

        <Card className="p-6">
          <div className="flex items-center gap-2 text-sm font-medium text-mist">
            <ArrowUpRight size={16} className="text-forest-500" />
            Total income
          </div>
          <div className="mt-4">
            <MoneyDisplay amount={summary?.income ?? 0} size="lg" tone="forest" />
          </div>
        </Card>

        <Card className="p-6">
          <div className="flex items-center gap-2 text-sm font-medium text-mist">
            <ArrowDownRight size={16} className="text-rust-500" />
            Total expenses
          </div>
          <div className="mt-4">
            <MoneyDisplay amount={summary?.expense ?? 0} size="lg" tone="rust" />
          </div>
        </Card>
      </div>

      {insight && (
        <Card className="mt-4 flex items-start gap-3 border-brass-300/60 bg-brass-100/30 p-4">
          <Sparkles size={18} className="mt-0.5 shrink-0 text-brass-600" />
          <p className="text-sm text-ink-soft">{insight}</p>
          <Link
            to="/insights"
            className="ml-auto shrink-0 whitespace-nowrap text-sm font-medium text-forest-500 hover:underline"
          >
            View all
          </Link>
        </Card>
      )}

      <div className="mt-4 grid gap-4 lg:grid-cols-5">
        <Card className="lg:col-span-3">
          <CardHeader title="30-day trend" subtitle="Income vs. expenses" />
          <div className="px-3 pb-4 pt-2">
            {trend.length ? (
              <TrendChart data={trend} />
            ) : (
              <EmptyState title="Not enough data yet" description="Trends appear once you log a few transactions." />
            )}
          </div>
        </Card>

        <Card className="lg:col-span-2">
          <CardHeader title="By category" subtitle="Where it's going" />
          <div className="p-5">
            <CategoryDonut data={categories} />
          </div>
        </Card>
      </div>

      <Card className="mt-4">
        <CardHeader
          title="Recent transactions"
          action={
            <Link to="/transactions" className="text-sm font-medium text-forest-500 hover:underline">
              View all
            </Link>
          }
        />
        <div className="mt-2 px-2 pb-2">
          {recent.length === 0 ? (
            <EmptyState
              icon={<Receipt size={28} />}
              title="No transactions yet"
              description="Log your first income or expense to get started."
              action={
                <Button size="sm" onClick={() => setAddOpen(true)}>
                  <Plus size={14} /> Add transaction
                </Button>
              }
            />
          ) : (
            <ul>
              {recent.map((t) => (
                <li
                  key={t.id}
                  className="tape-row flex items-center gap-4 px-3 py-3 last:bg-none"
                >
                  <div className="w-16 shrink-0 font-mono text-xs text-mist">
                    {formatDateShort(t.date)}
                  </div>
                  <div className="min-w-0 flex-1">
                    <p className="truncate text-sm font-medium text-ink">{t.description}</p>
                  </div>
                  <CategoryBadge category={t.category} />
                  <TypeBadge type={t.type} />
                  <div className="w-24 shrink-0 text-right font-mono tabular text-sm font-medium">
                    <span className={t.type === 'income' ? 'text-forest-500' : 'text-rust-500'}>
                      {t.type === 'income' ? '+' : '−'}
                      {formatMoney(Math.abs(t.amount))}
                    </span>
                  </div>
                </li>
              ))}
            </ul>
          )}
        </div>
      </Card>

      <TransactionFormModal
        open={addOpen}
        onClose={() => setAddOpen(false)}
        onSaved={() => {
          setAddOpen(false)
          loadAll()
        }}
      />
    </div>
  )
}
