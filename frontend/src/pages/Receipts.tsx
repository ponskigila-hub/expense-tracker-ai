import { useRef, useState } from 'react'
import { ScanLine, Upload, CheckCircle2, FileText } from 'lucide-react'
import { api, ApiError } from '@/lib/api'
import type { ReceiptScanResult } from '@/types'
import { PageHeader } from '@/components/ui/Misc'
import { Card, CardHeader } from '@/components/ui/Card'
import { Button } from '@/components/ui/Button'
import { MoneyDisplay } from '@/components/ui/MoneyDisplay'
import { CategoryBadge } from '@/components/ui/Misc'
import { useToast } from '@/context/ToastContext'

export default function Receipts() {
  const { notify } = useToast()
  const inputRef = useRef<HTMLInputElement>(null)
  const [file, setFile] = useState<File | null>(null)
  const [previewUrl, setPreviewUrl] = useState<string | null>(null)
  const [scanning, setScanning] = useState(false)
  const [result, setResult] = useState<ReceiptScanResult | null>(null)
  const [error, setError] = useState('')

  function handleFileChange(f: File | null) {
    setFile(f)
    setResult(null)
    setError('')
    setPreviewUrl(f ? URL.createObjectURL(f) : null)
  }

  async function handleScan() {
    if (!file) return
    setScanning(true)
    setError('')
    try {
      const res = await api.receipts.scan(file, true)
      setResult(res)
      if (res.saved) notify('Receipt scanned and transaction saved')
    } catch (err) {
      setError(err instanceof ApiError ? err.message : 'Could not scan this receipt.')
    } finally {
      setScanning(false)
    }
  }

  function reset() {
    handleFileChange(null)
    if (inputRef.current) inputRef.current.value = ''
  }

  return (
    <div>
      <PageHeader
        eyebrow="AI"
        title="Scan a receipt"
        description="Upload a photo and we'll pull out the merchant, amount, and category."
      />

      <div className="mb-6 overflow-hidden rounded-xl border border-mist-light/60 bg-surface/90 shadow-[0_4px_24px_rgba(0,0,0,0.35)]">
        <div className="relative h-48 w-full overflow-hidden">
          <img src="/ai_scan_banner.jpg" alt="AI Optical Receipt Scanner" className="h-full w-full object-cover object-center brightness-90" />
          <div className="absolute inset-0 bg-gradient-to-r from-[#0D0E13]/90 via-[#0D0E13]/60 to-transparent flex items-center p-8">
            <div className="max-w-md">
              <span className="text-xs font-mono font-bold uppercase tracking-widest text-forest-500">
                OCR Telemetry &amp; Intelligence
              </span>
              <h2 className="font-display text-2xl font-black uppercase text-ink mt-1">
                Precision Receipt Optical Scan
              </h2>
            </div>
          </div>
        </div>
      </div>

      <div className="grid gap-6 lg:grid-cols-2">
        <Card className="p-5">
          <input
            ref={inputRef}
            type="file"
            accept="image/*"
            className="hidden"
            onChange={(e) => handleFileChange(e.target.files?.[0] || null)}
          />

          {!previewUrl ? (
            <button
              onClick={() => inputRef.current?.click()}
              className="flex w-full flex-col items-center justify-center gap-3 rounded-lg border-2 border-dashed border-mist-light py-16 text-mist transition-colors hover:border-forest-500 hover:text-forest-500"
            >
              <ScanLine size={32} />
              <span className="text-sm font-medium">Click to choose a receipt photo</span>
              <span className="text-xs">JPG, PNG — clear, well-lit shots work best</span>
            </button>
          ) : (
            <div>
              <img src={previewUrl} alt="Receipt preview" className="max-h-80 w-full rounded-md object-contain" />
              <div className="mt-4 flex gap-2">
                <Button variant="secondary" onClick={reset} className="flex-1">Choose different photo</Button>
                <Button onClick={handleScan} disabled={scanning} className="flex-1">
                  <Upload size={15} /> {scanning ? 'Scanning…' : 'Scan receipt'}
                </Button>
              </div>
              {error && <p className="mt-3 text-sm text-rust-500">{error}</p>}
            </div>
          )}
        </Card>

        <Card>
          <CardHeader title="Result" subtitle={result ? undefined : 'Scan a receipt to see what we found'} />
          <div className="p-5">
            {!result ? (
              <div className="flex h-48 flex-col items-center justify-center gap-2 text-center text-mist">
                <FileText size={28} />
                <p className="text-sm">Nothing scanned yet</p>
              </div>
            ) : (
              <div className="space-y-4">
                {result.saved && (
                  <div className="flex items-center gap-2 rounded-md bg-forest-50 px-3 py-2 text-sm text-forest-600">
                    <CheckCircle2 size={16} />
                    Saved as a transaction
                  </div>
                )}

                <div>
                  <p className="text-xs font-medium uppercase tracking-wider text-mist">Merchant</p>
                  <p className="mt-0.5 text-sm font-medium text-ink">{result.merchant || 'Not detected'}</p>
                </div>

                <div>
                  <p className="text-xs font-medium uppercase tracking-wider text-mist">Amount</p>
                  {result.amount != null ? (
                    <MoneyDisplay amount={result.amount} size="lg" tone="rust" />
                  ) : (
                    <p className="mt-0.5 text-sm text-mist">Not detected</p>
                  )}
                </div>

                <div className="flex items-center gap-4">
                  <div>
                    <p className="text-xs font-medium uppercase tracking-wider text-mist">Date</p>
                    <p className="mt-0.5 text-sm text-ink">{result.date || 'Not detected'}</p>
                  </div>
                  <div>
                    <p className="text-xs font-medium uppercase tracking-wider text-mist">Category</p>
                    <div className="mt-1">
                      {result.category ? (
                        <div className="flex items-center gap-2">
                          <CategoryBadge category={result.category} />
                          {result.category_confidence != null && (
                            <span className="font-mono text-xs text-mist">
                              {Math.round(result.category_confidence * 100)}%
                            </span>
                          )}
                        </div>
                      ) : (
                        <p className="text-sm text-mist">Not detected</p>
                      )}
                    </div>
                  </div>
                </div>

                <details className="text-xs text-mist">
                  <summary className="cursor-pointer font-medium">Raw extracted text</summary>
                  <pre className="mt-2 max-h-40 overflow-y-auto whitespace-pre-wrap rounded-md bg-paper-dim p-3 font-mono text-[11px]">
                    {result.raw_text}
                  </pre>
                </details>
              </div>
            )}
          </div>
        </Card>
      </div>
    </div>
  )
}
