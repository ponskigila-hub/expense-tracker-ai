import { FormEvent, useEffect, useState } from 'react'
import { Plus, Trash2, PiggyBank, TriangleAlert } from 'lucide-react'
import { api, ApiError } from '@/lib/api'
import type { Budget } from '@/types'
import { PageHeader, Spinner, EmptyState, ProgressBar, CategoryBadge } from '@/components/ui/Misc'
import { Card } from '@/components/ui/Card'
import { Button } from '@/components/ui/Button'
import { Modal } from '@/components/ui/Modal'
import { Input, Select } from '@/components/ui/Input'
import { MoneyDisplay } from '@/components/ui/MoneyDisplay'
import { CATEGORIES } from '@/lib/format'
import { useToast } from '@/context/ToastContext'

export default function Budgets() {
  const { notify } = useToast()
  const [budgets, setBudgets] = useState<Budget[]>([])
  const [loading, setLoading] = useState(true)
  const [modalOpen, setModalOpen] = useState(false)

  async function load() {
    setLoading(true)
    try {
      setBudgets(await api.budgets.list())
    } finally {
      setLoading(false)
    }
  }

  useEffect(() => {
    load()
  }, [])

  async function handleDelete(id: number) {
    if (!confirm('Delete this budget?')) return
    await api.budgets.remove(id)
    notify('Budget deleted')
    load()
  }

  return (
    <div>
      <PageHeader
        eyebrow="Planning"
        title="Budgets"
        description="Set a limit per category and keep an eye on it."
        action={<Button onClick={() => setModalOpen(true)}><Plus size={16} /> New budget</Button>}
      />

      {loading ? (
        <div className="flex h-40 items-center justify-center"><Spinner className="h-5 w-5 text-forest-500" /></div>
      ) : budgets.length === 0 ? (
        <Card>
          <EmptyState
            icon={<PiggyBank size={28} />}
            title="No budgets yet"
            description="Create a budget for a category to start tracking against a limit."
            action={<Button size="sm" onClick={() => setModalOpen(true)}><Plus size={14} /> New budget</Button>}
          />
        </Card>
      ) : (
        <div className="grid gap-4 sm:grid-cols-2 lg:grid-cols-3">
          {budgets.map((b) => {
            const tone = b.is_exceeded ? 'rust' : b.percentage_used >= 80 ? 'brass' : 'forest'
            return (
              <Card key={b.id} className="p-5">
                <div className="flex items-start justify-between">
                  <CategoryBadge category={b.category} />
                  <button
                    onClick={() => handleDelete(b.id)}
                    className="rounded p-1 text-mist hover:bg-rust-100 hover:text-rust-600"
                    aria-label="Delete budget"
                  >
                    <Trash2 size={15} />
                  </button>
                </div>

                <div className="mt-4">
                  <MoneyDisplay amount={b.spent} size="md" tone={tone === 'rust' ? 'rust' : 'ink'} />
                  <span className="ml-1.5 font-mono text-xs text-mist">/ {b.amount.toFixed(2)} limit</span>
                </div>

                <div className="mt-3">
                  <ProgressBar value={b.percentage_used} tone={tone} />
                  <div className="mt-1.5 flex items-center justify-between text-xs text-mist">
                    <span>{b.percentage_used.toFixed(0)}% used</span>
                    <span>{formatRemaining(b.remaining)}</span>
                  </div>
                </div>

                {b.warning && (
                  <div className="mt-3 flex items-start gap-1.5 rounded-md bg-rust-100/60 px-2.5 py-2 text-xs text-rust-600">
                    <TriangleAlert size={13} className="mt-0.5 shrink-0" />
                    {b.warning}
                  </div>
                )}
              </Card>
            )
          })}
        </div>
      )}

      <NewBudgetModal
        open={modalOpen}
        onClose={() => setModalOpen(false)}
        onSaved={() => { setModalOpen(false); load() }}
        existingCategories={budgets.map((b) => b.category)}
      />
    </div>
  )
}

function formatRemaining(remaining: number) {
  return remaining >= 0
    ? `$${remaining.toFixed(2)} left`
    : `$${Math.abs(remaining).toFixed(2)} over`
}

function NewBudgetModal({
  open,
  onClose,
  onSaved,
  existingCategories,
}: {
  open: boolean
  onClose: () => void
  onSaved: () => void
  existingCategories: string[]
}) {
  const { notify } = useToast()
  const [category, setCategory] = useState('Food')
  const [amount, setAmount] = useState('')
  const [saving, setSaving] = useState(false)
  const [error, setError] = useState('')

  useEffect(() => {
    if (open) {
      setCategory('Food')
      setAmount('')
      setError('')
    }
  }, [open])

  async function handleSubmit(e: FormEvent) {
    e.preventDefault()
    setError('')
    setSaving(true)
    try {
      await api.budgets.create({ category, amount: Number(amount) })
      notify('Budget created')
      onSaved()
    } catch (err) {
      setError(err instanceof ApiError ? err.message : 'Could not create budget.')
    } finally {
      setSaving(false)
    }
  }

  return (
    <Modal open={open} onClose={onClose} title="New budget">
      <form onSubmit={handleSubmit} className="space-y-4">
        <Select label="Category" value={category} onChange={(e) => setCategory(e.target.value)}>
          {CATEGORIES.map((c) => (
            <option key={c} value={c} disabled={existingCategories.includes(c)}>
              {c}{existingCategories.includes(c) ? ' (already set)' : ''}
            </option>
          ))}
        </Select>
        <Input
          label="Monthly limit"
          type="number"
          step="0.01"
          min="0"
          required
          value={amount}
          onChange={(e) => setAmount(e.target.value)}
          placeholder="500.00"
        />
        {error && <p className="text-sm text-rust-500">{error}</p>}
        <div className="flex justify-end gap-2 pt-2">
          <Button type="button" variant="secondary" onClick={onClose}>Cancel</Button>
          <Button type="submit" disabled={saving}>{saving ? 'Saving…' : 'Create budget'}</Button>
        </div>
      </form>
    </Modal>
  )
}
