import { FormEvent, useEffect, useState } from 'react'
import { Sparkles } from 'lucide-react'
import { Modal } from '@/components/ui/Modal'
import { Input, Select, Textarea } from '@/components/ui/Input'
import { Button } from '@/components/ui/Button'
import { api, ApiError } from '@/lib/api'
import { CATEGORIES, todayISO } from '@/lib/format'
import { useToast } from '@/context/ToastContext'
import type { Transaction, TransactionType } from '@/types'

interface Props {
  open: boolean
  onClose: () => void
  onSaved: () => void
  transaction?: Transaction | null
}

const emptyForm = {
  date: todayISO(),
  description: '',
  amount: '',
  type: 'expense' as TransactionType,
  category: 'Food',
  notes: '',
}

export function TransactionFormModal({ open, onClose, onSaved, transaction }: Props) {
  const { notify } = useToast()
  const [form, setForm] = useState(emptyForm)
  const [saving, setSaving] = useState(false)
  const [suggesting, setSuggesting] = useState(false)
  const [error, setError] = useState('')

  useEffect(() => {
    if (open) {
      setError('')
      setForm(
        transaction
          ? {
              date: transaction.date,
              description: transaction.description,
              amount: String(transaction.amount),
              type: transaction.type,
              category: transaction.category,
              notes: transaction.notes || '',
            }
          : emptyForm
      )
    }
  }, [open, transaction])

  async function handleSuggestCategory() {
    if (!form.description.trim()) return
    setSuggesting(true)
    try {
      const result = await api.prediction.predictCategory(form.description)
      setForm((f) => ({ ...f, category: result.category }))
      notify(`Suggested "${result.category}" (${Math.round(result.confidence * 100)}% confident)`)
    } catch {
      notify('Could not get a suggestion right now', 'error')
    } finally {
      setSuggesting(false)
    }
  }

  async function handleSubmit(e: FormEvent) {
    e.preventDefault()
    setError('')
    setSaving(true)
    try {
      const payload = {
        date: form.date,
        description: form.description,
        amount: Number(form.amount),
        type: form.type,
        category: form.category,
        notes: form.notes || null,
      }
      if (transaction) {
        await api.transactions.update(transaction.id, payload)
        notify('Transaction updated')
      } else {
        await api.transactions.create(payload)
        notify('Transaction added')
      }
      onSaved()
    } catch (err) {
      setError(err instanceof ApiError ? err.message : 'Could not save transaction.')
    } finally {
      setSaving(false)
    }
  }

  return (
    <Modal open={open} onClose={onClose} title={transaction ? 'Edit transaction' : 'Add transaction'}>
      <form onSubmit={handleSubmit} className="space-y-4">
        <div className="grid grid-cols-2 gap-3">
          <Select
            label="Type"
            value={form.type}
            onChange={(e) => setForm({ ...form, type: e.target.value as TransactionType })}
          >
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
          placeholder="e.g. Starbucks coffee"
        />

        <div className="grid grid-cols-2 gap-3">
          <Input
            label="Date"
            type="date"
            required
            value={form.date}
            onChange={(e) => setForm({ ...form, date: e.target.value })}
          />
          <div>
            <div className="flex items-center justify-between">
              <span className="mb-1.5 block text-sm font-medium text-ink-soft">Category</span>
              <button
                type="button"
                onClick={handleSuggestCategory}
                disabled={suggesting || !form.description.trim()}
                className="mb-1.5 flex items-center gap-1 text-xs font-medium text-brass-600 hover:text-brass-500 disabled:opacity-40"
              >
                <Sparkles size={12} />
                {suggesting ? 'Thinking…' : 'AI suggest'}
              </button>
            </div>
            <Select
              value={form.category}
              onChange={(e) => setForm({ ...form, category: e.target.value })}
            >
              {CATEGORIES.map((c) => (
                <option key={c} value={c}>{c}</option>
              ))}
            </Select>
          </div>
        </div>

        <Textarea
          label="Notes (optional)"
          value={form.notes}
          onChange={(e) => setForm({ ...form, notes: e.target.value })}
        />

        {error && <p className="text-sm text-rust-500">{error}</p>}

        <div className="flex justify-end gap-2 pt-2">
          <Button type="button" variant="secondary" onClick={onClose}>Cancel</Button>
          <Button type="submit" disabled={saving}>
            {saving ? 'Saving…' : transaction ? 'Save changes' : 'Add transaction'}
          </Button>
        </div>
      </form>
    </Modal>
  )
}
