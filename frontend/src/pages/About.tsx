import { PageHeader } from '@/components/ui/Misc'
import { Card, CardHeader } from '@/components/ui/Card'
import { ShieldCheck, Sparkles, Cpu, Receipt, PiggyBank, LineChart, Lock } from 'lucide-react'

export default function About() {
  return (
    <div className="space-y-8">
      <PageHeader
        eyebrow="Platform"
        title="About Ledger"
        description="Next-generation financial intelligence platform built for modern personal wealth management and precise expense tracking."
      />

      {/* Hero Visual Section */}
      <div className="overflow-hidden rounded-2xl border border-mist-light/60 bg-surface shadow-[0_4px_24px_rgba(0,0,0,0.15)] dark:shadow-[0_4px_24px_rgba(0,0,0,0.35)]">
        <div className="relative h-64 w-full overflow-hidden">
          <img src="/hero_telemetry.jpg" alt="Ledger Financial Telemetry" className="h-full w-full object-cover object-center brightness-90" />
          <div className="absolute inset-0 bg-gradient-to-r from-paper/95 via-paper/70 to-transparent p-8 md:p-12 flex flex-col justify-center">
            <div className="max-w-xl space-y-3">
              <span className="inline-flex items-center gap-2 rounded-full border border-forest-500/30 bg-forest-500/10 px-3 py-1 text-xs font-mono font-bold uppercase tracking-widest text-forest-500">
                <Sparkles size={14} /> Driven by AI &amp; Telemetry
              </span>
              <h2 className="font-display text-3xl font-extrabold uppercase text-ink">
                Intelligent Wealth Control
              </h2>
              <p className="text-sm leading-relaxed text-ink-soft">
                Ledger combines high-performance transaction telemetry, automated OCR receipt scanning, and budget forecasting into a seamless experience.
              </p>
            </div>
          </div>
        </div>
      </div>

      {/* Core Values Grid */}
      <div className="grid gap-6 md:grid-cols-3">
        <Card className="p-6 space-y-3">
          <div className="p-3 w-fit rounded-xl bg-forest-500/10 text-forest-500 border border-forest-500/20">
            <Cpu size={24} />
          </div>
          <h3 className="font-display text-lg font-bold uppercase text-ink">AI Categorization</h3>
          <p className="text-sm text-ink-soft leading-relaxed">
            Automatic transaction analysis accurately tags merchants and sector categories, minimizing manual entry.
          </p>
        </Card>

        <Card className="p-6 space-y-3">
          <div className="p-3 w-fit rounded-xl bg-brass-500/10 text-brass-500 border border-brass-500/20">
            <Receipt size={24} />
          </div>
          <h3 className="font-display text-lg font-bold uppercase text-ink">OCR Receipt Scan</h3>
          <p className="text-sm text-ink-soft leading-relaxed">
            Scan physical paper receipts in seconds. Our optical engine parses store names, itemized totals, and dates seamlessly.
          </p>
        </Card>

        <Card className="p-6 space-y-3">
          <div className="p-3 w-fit rounded-xl bg-forest-500/10 text-forest-500 border border-forest-500/20">
            <ShieldCheck size={24} />
          </div>
          <h3 className="font-display text-lg font-bold uppercase text-ink">Privacy &amp; Security</h3>
          <p className="text-sm text-ink-soft leading-relaxed">
            Your financial data is encrypted and strictly isolated. No selling of personal data, ever.
          </p>
        </Card>
      </div>

      {/* Platform Features Details */}
      <Card>
        <CardHeader title="System Capabilities" subtitle="Engineered for accuracy and clarity" />
        <div className="p-6 grid gap-6 md:grid-cols-2">
          <div className="flex items-start gap-4">
            <div className="p-2 rounded-lg bg-surface border border-mist-light text-forest-500">
              <PiggyBank size={20} />
            </div>
            <div>
              <h4 className="text-sm font-bold uppercase text-ink">Budget Telemetry</h4>
              <p className="text-xs text-ink-soft mt-1 leading-relaxed">
                Set monthly spending caps per category with real-time visual progress monitoring and threshold warnings.
              </p>
            </div>
          </div>

          <div className="flex items-start gap-4">
            <div className="p-2 rounded-lg bg-surface border border-mist-light text-forest-500">
              <LineChart size={20} />
            </div>
            <div>
              <h4 className="text-sm font-bold uppercase text-ink">Trend Analysis</h4>
              <p className="text-xs text-ink-soft mt-1 leading-relaxed">
                Interactive monthly and quarterly charts visualizing income versus expense distributions over time.
              </p>
            </div>
          </div>

          <div className="flex items-start gap-4">
            <div className="p-2 rounded-lg bg-surface border border-mist-light text-forest-500">
              <Lock size={20} />
            </div>
            <div>
              <h4 className="text-sm font-bold uppercase text-ink">Secure Exports</h4>
              <p className="text-xs text-ink-soft mt-1 leading-relaxed">
                Export your ledger data to CSV or JSON formats at any time for tax preparation or custom modeling.
              </p>
            </div>
          </div>

          <div className="flex items-start gap-4">
            <div className="p-2 rounded-lg bg-surface border border-mist-light text-forest-500">
              <Sparkles size={20} />
            </div>
            <div>
              <h4 className="text-sm font-bold uppercase text-ink">AI Insights Engine</h4>
              <p className="text-xs text-ink-soft mt-1 leading-relaxed">
                Receive personalized financial suggestions and anomaly alerts based on your real spending habits.
              </p>
            </div>
          </div>
        </div>
      </Card>
    </div>
  )
}
