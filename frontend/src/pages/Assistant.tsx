import { FormEvent, useEffect, useRef, useState } from 'react'
import { BrainCircuit, ListChecks, MessageCircle, Send, Sparkles } from 'lucide-react'
import clsx from 'clsx'
import { api, ApiError } from '@/lib/api'
import type { ChatMessage } from '@/types'
import { PageHeader, Spinner } from '@/components/ui/Misc'
import { Card } from '@/components/ui/Card'
import { Button } from '@/components/ui/Button'

interface DisplayMessage extends ChatMessage {
  generatedBy?: 'llm' | 'rule_based'
}

const SUGGESTIONS = [
  'How much did I spend this month?',
  'What was my biggest expense last week?',
  'How is my budget doing?',
  'Am I spending more than usual?',
]

export default function Assistant() {
  const [messages, setMessages] = useState<DisplayMessage[]>([])
  const [input, setInput] = useState('')
  const [sending, setSending] = useState(false)
  const [error, setError] = useState('')
  const bottomRef = useRef<HTMLDivElement>(null)

  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: 'smooth' })
  }, [messages, sending])

  async function send(text: string) {
    const trimmed = text.trim()
    if (!trimmed || sending) return

    setError('')
    const history = messages.map(({ role, content }) => ({ role, content }))
    setMessages((prev) => [...prev, { role: 'user', content: trimmed }])
    setInput('')
    setSending(true)

    try {
      const res = await api.assistant.ask(trimmed, history)
      setMessages((prev) => [
        ...prev,
        { role: 'assistant', content: res.reply, generatedBy: res.generated_by },
      ])
    } catch (err) {
      setError(err instanceof ApiError ? err.message : 'Something went wrong reaching the assistant.')
    } finally {
      setSending(false)
    }
  }

  function handleSubmit(e: FormEvent) {
    e.preventDefault()
    send(input)
  }

  return (
    <div className="flex h-[calc(100vh-8rem)] flex-col">
      <PageHeader
        eyebrow="AI"
        title="Assistant"
        description="Ask questions about your spending, budgets, and income in plain language."
      />

      <Card className="flex flex-1 flex-col overflow-hidden">
        <div className="flex-1 space-y-4 overflow-y-auto p-5">
          {messages.length === 0 && (
            <div className="flex h-full flex-col items-center justify-center gap-4 text-center">
              <div className="flex h-12 w-12 items-center justify-center rounded-full bg-brass-100 text-brass-600">
                <MessageCircle size={22} />
              </div>
              <div>
                <p className="font-display text-lg font-medium tracking-tight text-ink">
                  Ask me about your finances
                </p>
                <p className="mt-1 max-w-sm text-sm leading-relaxed text-mist">
                  I can only see your own transactions, budgets, and income — try one of these to
                  get started.
                </p>
              </div>
              <div className="flex flex-wrap justify-center gap-2">
                {SUGGESTIONS.map((s) => (
                  <button
                    key={s}
                    onClick={() => send(s)}
                    className="rounded-full border border-mist-light px-3 py-1.5 text-xs font-medium text-ink-soft transition-colors hover:border-forest-500 hover:text-forest-500"
                  >
                    {s}
                  </button>
                ))}
              </div>
            </div>
          )}

          {messages.map((m, i) => (
            <div
              key={i}
              className={clsx('flex', m.role === 'user' ? 'justify-end' : 'justify-start')}
            >
              <div
                className={clsx(
                  'max-w-[80%] rounded-lg px-4 py-2.5 text-sm leading-relaxed',
                  m.role === 'user'
                    ? 'bg-forest-500 text-white'
                    : 'border border-brass-300/60 bg-brass-100/30 text-ink-soft'
                )}
              >
                {m.role === 'assistant' && (
                  <div className="mb-1 flex items-center gap-1.5 text-[11px] font-medium text-brass-600">
                    {m.generatedBy === 'llm' ? <BrainCircuit size={12} /> : <ListChecks size={12} />}
                    {m.generatedBy === 'llm' ? 'AI model' : 'Rule-based'}
                  </div>
                )}
                <p className="whitespace-pre-wrap">{m.content}</p>
              </div>
            </div>
          ))}

          {sending && (
            <div className="flex justify-start">
              <div className="flex items-center gap-2 rounded-lg border border-brass-300/60 bg-brass-100/30 px-4 py-2.5 text-sm text-mist">
                <Spinner className="h-3.5 w-3.5" />
                Thinking…
              </div>
            </div>
          )}

          {error && (
            <div className="flex justify-start">
              <div className="rounded-lg border border-rust-100 bg-rust-100/20 px-4 py-2.5 text-sm text-rust-600">
                {error}
              </div>
            </div>
          )}

          <div ref={bottomRef} />
        </div>

        <form
          onSubmit={handleSubmit}
          className="flex items-center gap-2 border-t border-mist-light/60 p-3"
        >
          <input
            value={input}
            onChange={(e) => setInput(e.target.value)}
            placeholder="Ask about your spending…"
            className="h-10 flex-1 rounded border border-mist-light bg-surface px-3 text-sm text-ink placeholder:text-mist focus:border-forest-500 focus:outline-none focus:ring-1 focus:ring-forest-500"
            disabled={sending}
          />
          <Button type="submit" disabled={sending || !input.trim()} aria-label="Send">
            <Send size={16} />
          </Button>
        </form>
      </Card>

      <p className="mt-2 flex items-center gap-1.5 text-xs text-mist">
        <Sparkles size={12} />
        Answers are generated from your own data and may occasionally be imprecise.
      </p>
    </div>
  )
}
