import { useEffect, useState } from 'react'
import { Plus, Search, Pencil, Trash2 } from 'lucide-react'
import { api } from '@/lib/api'
import type { PaginatedTransactions, Transaction, TransactionFilters } from '@/types'
import { PageHeader, Spinner, EmptyState, CategoryBadge, TypeBadge } from '@/components/ui/Misc'
import { Card } from '@/components/ui/Card'
import { Button } from '@/components/ui/Button'
import { Input, Select } from '@/components/ui/Input'
import { formatDate, formatMoney, CATEGORIES } from '@/lib/format'
import { useToast } from '@/context/ToastContext'
import { TransactionFormModal } from './TransactionFormModal'

export default function Transactions() {
  const { notify } = useToast()
  const [data, setData] = useState<PaginatedTransactions | null>(null)
  const [loading, setLoading] = useState(true)
  const [filters, setFilters] = useState<TransactionFilters>({ page: 1, page_size: 20 })
  const [modalTxn, setModalTxn] = useState<Transaction | null | undefined>(undefined)

  async function load() {
    setLoading(true)
    try {
      const result = await api.transactions.list(filters)
      setData(result)
    } finally {
      setLoading(false)
    }
  }

  useEffect(() => {
    load()
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [filters])

  function updateFilter<K extends keyof TransactionFilters>(key: K, value: TransactionFilters[K]) {
    setFilters((prev) => ({ ...prev, [key]: value || undefined, page: 1 }))
  }

  async function handleDelete(id: number) {
    if (!confirm('Delete this transaction? This cannot be undone.')) return
    await api.transactions.remove(id)
    notify('Transaction deleted')
    load()
  }

  return (
    <div>
      <PageHeader
        eyebrow="Ledger"
        title="Transactions"
        description={data ? `${data.total} total` : undefined}
        action={<Button onClick={() => setModalTxn(null)}><Plus size={16} /> Add transaction</Button>}
      />

      <Card className="mb-4 flex flex-wrap gap-3 p-4">
        <Input
          className="min-w-[200px] flex-1"
          placeholder="Search description…"
          onChange={(e) => updateFilter('search', e.target.value)}
        />
        <Select className="w-40" onChange={(e) => updateFilter('type', (e.target.value || undefined) as any)}>
          <option value="">All types</option>
          <option value="income">Income</option>
          <option value="expense">Expense</option>
        </Select>
        <Select className="w-44" onChange={(e) => updateFilter('category', e.target.value)}>
          <option value="">All categories</option>
          {CATEGORIES.map((c) => <option key={c} value={c}>{c}</option>)}
        </Select>
        <Select
          className="w-48"
          onChange={(e) => {
            const [sort_by, sort_order] = e.target.value.split(':') as any
            setFilters((prev) => ({ ...prev, sort_by, sort_order, page: 1 }))
          }}
        >
          <option value="date:desc">Newest first</option>
          <option value="date:asc">Oldest first</option>
          <option value="amount:desc">Amount: high to low</option>
          <option value="amount:asc">Amount: low to high</option>
        </Select>
      </Card>

      <Card>
        {loading ? (
          <div className="flex h-40 items-center justify-center"><Spinner className="h-5 w-5 text-forest-500" /></div>
        ) : !data || data.items.length === 0 ? (
          <EmptyState
            icon={<Search size={28} />}
            title="No transactions match"
            description="Try clearing a filter, or add your first transaction."
          />
        ) : (
          <>
            <ul>
              {data.items.map((t) => (
                <li key={t.id} className="tape-row group flex items-center gap-4 px-4 py-3">
                  <div className="w-24 shrink-0 font-mono text-xs text-mist">{formatDate(t.date)}</div>
                  <div className="min-w-0 flex-1">
                    <p className="truncate text-sm font-medium text-ink">{t.description}</p>
                    {t.notes && <p className="truncate text-xs text-mist">{t.notes}</p>}
                  </div>
                  <CategoryBadge category={t.category} />
                  <TypeBadge type={t.type} />
                  <div className="w-24 shrink-0 text-right font-mono tabular text-sm font-medium">
                    <span className={t.type === 'income' ? 'text-forest-500' : 'text-rust-500'}>
                      {t.type === 'income' ? '+' : '−'}
                      {formatMoney(Math.abs(t.amount))}
                    </span>
                  </div>
                  <div className="flex shrink-0 gap-1 opacity-0 transition-opacity group-hover:opacity-100">
                    <button
                      onClick={() => setModalTxn(t)}
                      className="rounded p-1.5 text-mist hover:bg-paper-dim hover:text-ink"
                      aria-label="Edit"
                    >
                      <Pencil size={15} />
                    </button>
                    <button
                      onClick={() => handleDelete(t.id)}
                      className="rounded p-1.5 text-mist hover:bg-rust-100 hover:text-rust-600"
                      aria-label="Delete"
                    >
                      <Trash2 size={15} />
                    </button>
                  </div>
                </li>
              ))}
            </ul>

            {data.total_pages > 1 && (
              <div className="flex items-center justify-between border-t border-mist-light px-4 py-3 text-sm">
                <span className="text-mist">Page {data.page} of {data.total_pages}</span>
                <div className="flex gap-2">
                  <Button
                    variant="secondary" size="sm"
                    disabled={data.page <= 1}
                    onClick={() => setFilters((p) => ({ ...p, page: (p.page || 1) - 1 }))}
                  >Previous</Button>
                  <Button
                    variant="secondary" size="sm"
                    disabled={data.page >= data.total_pages}
                    onClick={() => setFilters((p) => ({ ...p, page: (p.page || 1) + 1 }))}
                  >Next</Button>
                </div>
              </div>
            )}
          </>
        )}
      </Card>

      <TransactionFormModal
        open={modalTxn !== undefined}
        transaction={modalTxn}
        onClose={() => setModalTxn(undefined)}
        onSaved={() => { setModalTxn(undefined); load() }}
      />
    </div>
  )
}
