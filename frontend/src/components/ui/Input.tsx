import { InputHTMLAttributes, SelectHTMLAttributes, forwardRef, TextareaHTMLAttributes } from 'react'
import clsx from 'clsx'
import { ChevronDown } from 'lucide-react'

interface FieldWrapProps {
  label?: string
  error?: string
  hint?: string
  className?: string
}

const fieldBase =
  'w-full rounded border border-mist-light bg-surface px-3 h-10 text-sm text-ink placeholder:text-mist focus:border-forest-500 focus:outline-none focus:ring-1 focus:ring-forest-500 disabled:bg-paper-dim disabled:text-mist'

interface InputProps
  extends InputHTMLAttributes<HTMLInputElement>,
    FieldWrapProps {}

export const Input = forwardRef<HTMLInputElement, InputProps>(
  ({ label, error, hint, className, id, ...props }, ref) => {
    const inputId = id || props.name
    return (
      <label className={clsx('block', className)} htmlFor={inputId}>
        {label && (
          <span className="mb-1.5 block text-sm font-medium text-ink-soft">{label}</span>
        )}
        <input ref={ref} id={inputId} className={fieldBase} {...props} />
        {hint && !error && <span className="mt-1 block text-xs text-mist">{hint}</span>}
        {error && <span className="mt-1 block text-xs text-rust-500">{error}</span>}
      </label>
    )
  }
)
Input.displayName = 'Input'

interface SelectProps
  extends SelectHTMLAttributes<HTMLSelectElement>,
    FieldWrapProps {}

export const Select = forwardRef<HTMLSelectElement, SelectProps>(
  ({ label, error, className, id, children, ...props }, ref) => {
    const selectId = id || props.name
    return (
      <label className={clsx('block', className)} htmlFor={selectId}>
        {label && (
          <span className="mb-1.5 block text-sm font-medium text-ink-soft">{label}</span>
        )}
        <div className="relative">
          <select
            ref={ref}
            id={selectId}
            className={clsx(fieldBase, 'appearance-none pr-9')}
            {...props}
          >
            {children}
          </select>
          <ChevronDown
            size={16}
            className="pointer-events-none absolute right-3 top-1/2 -translate-y-1/2 text-mist"
          />
        </div>
        {error && <span className="mt-1 block text-xs text-rust-500">{error}</span>}
      </label>
    )
  }
)
Select.displayName = 'Select'

interface TextareaProps
  extends TextareaHTMLAttributes<HTMLTextAreaElement>,
    FieldWrapProps {}

export const Textarea = forwardRef<HTMLTextAreaElement, TextareaProps>(
  ({ label, error, className, id, ...props }, ref) => {
    const areaId = id || props.name
    return (
      <label className={clsx('block', className)} htmlFor={areaId}>
        {label && (
          <span className="mb-1.5 block text-sm font-medium text-ink-soft">{label}</span>
        )}
        <textarea
          ref={ref}
          id={areaId}
          className={clsx(fieldBase, 'h-auto min-h-[80px] py-2')}
          {...props}
        />
        {error && <span className="mt-1 block text-xs text-rust-500">{error}</span>}
      </label>
    )
  }
)
Textarea.displayName = 'Textarea'
