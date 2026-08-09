import { FormEvent, useEffect, useState } from 'react'
import { Plus, Repeat, Trash2, Pencil, Play } from 'lucide-react'
import { api, ApiError } from '@/lib/api'
import type { RecurringTransaction, TransactionType } from '@/types'
import { PageHeader, Spinner, EmptyState, CategoryBadge, TypeBadge } from '@/components/ui/Misc'
import { Card } from '@/components/ui/Card'
import { Button } from '@/components/ui/Button'
import { Modal } from '@/components/ui/Modal'
import { Input, Select, Textarea } from '@/components/ui/Input'
import { formatMoney, CATEGORIES } from '@/lib/format'
import { useToast } from '@/context/ToastContext'

export default function Recurring() {
  const { notify } = useToast()
  const [items, setItems] = useState<RecurringTransaction[]>([])
  const [loading, setLoading] = useState(true)
  const [running, setRunning] = useState(false)
  const [modalItem, setModalItem] = useState<RecurringTransaction | null | undefined>(undefined)

  async function load() {
    setLoading(true)
    try {
      setItems(await api.recurring.list())
    } finally {
      setLoading(false)
    }
  }

  useEffect(() => {
    load()
  }, [])

  async function handleToggleActive(item: RecurringTransaction) {
    await api.recurring.update(item.id, { is_active: !item.is_active })
    load()
  }

  async function handleDelete(id: number) {
    if (!confirm('Delete this recurring transaction?')) return
    await api.recurring.remove(id)
    notify('Recurring transaction deleted')
    load()
  }

  async function handleRunNow() {
    setRunning(true)
    try {
      const created = await api.recurring.runNow()
      notify(`Created ${created.length} transaction${created.length === 1 ? '' : 's'}`)
      load()
    } catch (err) {
      notify(err instanceof ApiError ? err.message : 'Could not run recurring transactions.', 'error')
    } finally {
      setRunning(false)
    }
  }

  return (
    <div>
      <PageHeader
        eyebrow="Automation"
        title="Recurring transactions"
        description="Bills and income that repeat every month."
        action={
          <div className="flex gap-2">
            <Button variant="secondary" onClick={handleRunNow} disabled={running}>
              <Play size={15} /> {running ? 'Running…' : 'Run now'}
            </Button>
            <Button onClick={() => setModalItem(null)}><Plus size={16} /> New recurring</Button>
          </div>
        }
      />

      <Card>
        {loading ? (
          <div className="flex h-40 items-center justify-center"><Spinner className="h-5 w-5 text-forest-500" /></div>
        ) : items.length === 0 ? (
          <EmptyState
            icon={<Repeat size={28} />}
            title="No recurring transactions"
            description="Set up rent, subscriptions, or salary to auto-log every month."
            action={<Button size="sm" onClick={() => setModalItem(null)}><Plus size={14} /> New recurring</Button>}
          />
        ) : (
          <ul>
            {items.map((item) => (
              <li key={item.id} className="tape-row group flex items-center gap-4 px-4 py-3">
                <label className="flex shrink-0 items-center">
                  <input
                    type="checkbox"
                    checked={item.is_active}
                    onChange={() => handleToggleActive(item)}
                    className="h-4 w-4 rounded border-mist-light text-forest-500 focus:ring-forest-500"
                    aria-label={item.is_active ? 'Active' : 'Paused'}
                  />
                </label>
                <div className="w-16 shrink-0 font-mono text-xs text-mist">Day {item.day_of_month}</div>
                <div className="min-w-0 flex-1">
                  <p className={`truncate text-sm font-medium ${item.is_active ? 'text-ink' : 'text-mist line-through'}`}>
                    {item.description}
                  </p>
                  {item.last_run_date && (
                    <p className="truncate text-xs text-mist">Last run {item.last_run_date}</p>
                  )}
                </div>
                <CategoryBadge category={item.category} />
                <TypeBadge type={item.type} />
                <div className="w-24 shrink-0 text-right font-mono tabular text-sm font-medium">
                  <span className={item.type === 'income' ? 'text-forest-500' : 'text-rust-500'}>
                    {item.type === 'income' ? '+' : '−'}
                    {formatMoney(Math.abs(item.amount))}
                  </span>
                </div>
                <div className="flex shrink-0 gap-1 opacity-0 transition-opacity group-hover:opacity-100">
                  <button
                    onClick={() => setModalItem(item)}
                    className="rounded p-1.5 text-mist hover:bg-paper-dim hover:text-ink"
                    aria-label="Edit"
                  >
                    <Pencil size={15} />
                  </button>
                  <button
                    onClick={() => handleDelete(item.id)}
                    className="rounded p-1.5 text-mist hover:bg-rust-100 hover:text-rust-600"
                    aria-label="Delete"
                  >
                    <Trash2 size={15} />
                  </button>
                </div>
              </li>
            ))}
          </ul>
        )}
      </Card>

      <RecurringFormModal
        open={modalItem !== undefined}
        item={modalItem}
        onClose={() => setModalItem(undefined)}
        onSaved={() => { setModalItem(undefined); load() }}
      />
    </div>
  )
}

function RecurringFormModal({
  open,
  item,
  onClose,
  onSaved,
}: {
  open: boolean
  item?: RecurringTransaction | null
  onClose: () => void
  onSaved: () => void
}) {
  const { notify } = useToast()
  const emptyForm = {
    description: '',
    amount: '',
    type: 'expense' as TransactionType,
    category: 'Bills',
    notes: '',
    day_of_month: '1',
  }
  const [form, setForm] = useState(emptyForm)
  const [saving, setSaving] = useState(false)
  const [error, setError] = useState('')

  useEffect(() => {
    if (open) {
      setError('')
      setForm(
        item
          ? {
              description: item.description,
              amount: String(item.amount),
              type: item.type,
              category: item.category,
              notes: item.notes || '',
              day_of_month: String(item.day_of_month),
            }
          : emptyForm
      )
    }
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [open, item])

  async function handleSubmit(e: FormEvent) {
    e.preventDefault()
    setError('')
    setSaving(true)
    try {
      const payload = {
        description: form.description,
        amount: Number(form.amount),
        type: form.type,
        category: form.category,
        notes: form.notes || null,
        day_of_month: Number(form.day_of_month),
      }
      if (item) {
        await api.recurring.update(item.id, payload)
        notify('Recurring transaction updated')
      } else {
        await api.recurring.create(payload)
        notify('Recurring transaction created')
      }
      onSaved()
    } catch (err) {
      setError(err instanceof ApiError ? err.message : 'Could not save.')
    } finally {
      setSaving(false)
    }
  }

  return (
    <Modal open={open} onClose={onClose} title={item ? 'Edit recurring transaction' : 'New recurring transaction'}>
      <form onSubmit={handleSubmit} className="space-y-4">
        <div className="grid grid-cols-2 gap-3">
          <Select label="Type" value={form.type} onChange={(e) => setForm({ ...form, type: e.target.value as TransactionType })}>
            <option value="expense">Expense</option>
            <option value="income">Income</option>
          </Select>
          <Input
            label="Amount"
            type="number"
            step="0.01"
            min="0"
            required
            value={form.amount}
            onChange={(e) => setForm({ ...form, amount: e.target.value })}
          />
        </div>

        <Input
          label="Description"
          required
          value={form.description}
          onChange={(e) => setForm({ ...form, description: e.target.value })}
          placeholder="e.g. Rent, Netflix, Salary"
        />

        <div className="grid grid-cols-2 gap-3">
          <Input
            label="Day of month"
            type="number"
            min={1}
            max={28}
            required
            value={form.day_of_month}
            onChange={(e) => setForm({ ...form, day_of_month: e.target.value })}
            hint="1–28, so it always applies (even in February)."
          />
          <Select label="Category" value={form.category} onChange={(e) => setForm({ ...form, category: e.target.value })}>
            {CATEGORIES.map((c) => <option key={c} value={c}>{c}</option>)}
          </Select>
        </div>

        <Textarea
          label="Notes (optional)"
          value={form.notes}
          onChange={(e) => setForm({ ...form, notes: e.target.value })}
        />

        {error && <p className="text-sm text-rust-500">{error}</p>}

        <div className="flex justify-end gap-2 pt-2">
          <Button type="button" variant="secondary" onClick={onClose}>Cancel</Button>
          <Button type="submit" disabled={saving}>{saving ? 'Saving…' : item ? 'Save changes' : 'Create'}</Button>
        </div>
      </form>
    </Modal>
  )
}
