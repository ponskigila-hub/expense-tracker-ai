import { createContext, useCallback, useContext, useState, ReactNode } from 'react'
import { CheckCircle2, AlertCircle } from 'lucide-react'
import clsx from 'clsx'

interface Toast {
  id: number
  message: string
  tone: 'success' | 'error'
}

interface ToastContextValue {
  notify: (message: string, tone?: 'success' | 'error') => void
}

const ToastContext = createContext<ToastContextValue | undefined>(undefined)

export function ToastProvider({ children }: { children: ReactNode }) {
  const [toasts, setToasts] = useState<Toast[]>([])

  const notify = useCallback((message: string, tone: 'success' | 'error' = 'success') => {
    const id = Date.now() + Math.random()
    setToasts((prev) => [...prev, { id, message, tone }])
    setTimeout(() => {
      setToasts((prev) => prev.filter((t) => t.id !== id))
    }, 3500)
  }, [])

  return (
    <ToastContext.Provider value={{ notify }}>
      {children}
      <div className="pointer-events-none fixed bottom-5 right-5 z-[100] flex flex-col gap-2">
        {toasts.map((t) => (
          <div
            key={t.id}
            className={clsx(
              'pointer-events-auto flex items-center gap-2 rounded-lg border px-4 py-3 text-sm shadow-pop',
              t.tone === 'success'
                ? 'border-forest-100 bg-surface text-forest-600'
                : 'border-rust-100 bg-surface text-rust-600'
            )}
          >
            {t.tone === 'success' ? <CheckCircle2 size={16} /> : <AlertCircle size={16} />}
            {t.message}
          </div>
        ))}
      </div>
    </ToastContext.Provider>
  )
}

export function useToast() {
  const ctx = useContext(ToastContext)
  if (!ctx) throw new Error('useToast must be used within ToastProvider')
  return ctx
}
