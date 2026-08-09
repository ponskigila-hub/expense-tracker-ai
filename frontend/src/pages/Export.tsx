import { useState } from 'react'
import { FileSpreadsheet, FileText, FileDown } from 'lucide-react'
import { api, ApiError } from '@/lib/api'
import { PageHeader } from '@/components/ui/Misc'
import { Card, CardHeader } from '@/components/ui/Card'
import { Button } from '@/components/ui/Button'
import { Input } from '@/components/ui/Input'
import { useToast } from '@/context/ToastContext'

const formats: { key: 'csv' | 'excel' | 'pdf'; label: string; description: string; icon: typeof FileText }[] = [
  { key: 'csv', label: 'CSV', description: 'Plain spreadsheet data, opens anywhere.', icon: FileText },
  { key: 'excel', label: 'Excel', description: 'Formatted .xlsx workbook.', icon: FileSpreadsheet },
  { key: 'pdf', label: 'PDF', description: 'A printable statement-style report.', icon: FileDown },
]

export default function ExportPage() {
  const { notify } = useToast()
  const [dateFrom, setDateFrom] = useState('')
  const [dateTo, setDateTo] = useState('')
  const [downloading, setDownloading] = useState<string | null>(null)

  async function handleExport(format: 'csv' | 'excel' | 'pdf') {
    setDownloading(format)
    try {
      await api.export.download(format, {
        date_from: dateFrom || undefined,
        date_to: dateTo || undefined,
      })
      notify(`${format.toUpperCase()} downloaded`)
    } catch (err) {
      notify(err instanceof ApiError ? err.message : 'Export failed.', 'error')
    } finally {
      setDownloading(null)
    }
  }

  return (
    <div>
      <PageHeader
        eyebrow="Records"
        title="Export"
        description="Download your transactions for your records or another tool."
      />

      <Card className="max-w-2xl">
        <CardHeader title="Date range" subtitle="Leave blank to export everything" />
        <div className="grid grid-cols-2 gap-3 p-5 pt-3">
          <Input label="From" type="date" value={dateFrom} onChange={(e) => setDateFrom(e.target.value)} />
          <Input label="To" type="date" value={dateTo} onChange={(e) => setDateTo(e.target.value)} />
        </div>

        <div className="grid gap-3 border-t border-mist-light p-5 sm:grid-cols-3">
          {formats.map(({ key, label, description, icon: Icon }) => (
            <div key={key} className="flex flex-col justify-between rounded-md border border-mist-light p-4">
              <div>
                <Icon size={20} className="text-forest-500" />
                <p className="mt-2 text-sm font-medium text-ink">{label}</p>
                <p className="mt-1 text-xs text-mist">{description}</p>
              </div>
              <Button
                variant="secondary"
                size="sm"
                className="mt-4 w-full"
                onClick={() => handleExport(key)}
                disabled={downloading === key}
              >
                {downloading === key ? 'Downloading…' : `Export ${label}`}
              </Button>
            </div>
          ))}
        </div>
      </Card>
    </div>
  )
}
