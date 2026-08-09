import { useState } from 'react'
import { Link } from 'react-router-dom'
import { ArrowUpRight, Mail, ShieldCheck, Sparkles, CheckCircle2, ChevronUp } from 'lucide-react'

export function Footer() {
  const [copied, setCopied] = useState(false)

  function handleCopyContact() {
    navigator.clipboard.writeText('support@ledger.ai')
    setCopied(true)
    setTimeout(() => setCopied(false), 2000)
  }

  function scrollToTop() {
    window.scrollTo({ top: 0, behavior: 'smooth' })
  }

  return (
    <footer className="mt-20 border-t border-mist-light/60 bg-surface/90 dark:bg-[#0A0B0F] text-ink relative overflow-hidden">
      <div className="mx-auto max-w-7xl px-6 py-12 md:px-8">
        <div className="grid gap-10 lg:grid-cols-4">
          {/* Brand Column */}
          <div className="space-y-4">
            <div className="flex items-center gap-3">
              <div className="flex h-9 w-9 items-center justify-center rounded-xl bg-gradient-to-br from-forest-500 to-forest-700 shadow-[0_0_15px_rgba(195,65,30,0.4)] border border-forest-300/40">
                <div className="flex flex-col gap-[3px] items-center">
                  <span className="block h-[2.5px] w-4.5 rounded-full bg-white" />
                  <span className="block h-[2.5px] w-2.5 rounded-full bg-brass-300" />
                </div>
              </div>
              <span className="font-display text-2xl font-black tracking-tight uppercase">
                LEDGER
              </span>
            </div>
            <p className="text-sm text-ink-soft leading-relaxed">
              AI-powered financial intelligence and expense management platform.
            </p>
            <div className="flex items-center gap-3 text-xs font-mono text-mist uppercase tracking-widest pt-1">
              <span className="flex items-center gap-1.5 text-forest-500 font-semibold">
                <ShieldCheck size={15} /> Encrypted
              </span>
              <span>•</span>
              <span className="flex items-center gap-1.5 text-brass-500 font-semibold">
                <Sparkles size={15} /> AI Telemetry
              </span>
            </div>
          </div>

          {/* Core Navigation Column */}
          <div className="space-y-3">
            <p className="text-xs font-mono font-bold uppercase tracking-widest text-forest-500">
              Navigation
            </p>
            <ul className="space-y-2 text-xs font-semibold uppercase tracking-wider text-ink-soft">
              <li>
                <Link to="/" className="hover:text-forest-500 transition-colors flex items-center gap-1">
                  Dashboard <ArrowUpRight size={12} />
                </Link>
              </li>
              <li>
                <Link to="/transactions" className="hover:text-forest-500 transition-colors flex items-center gap-1">
                  Transactions <ArrowUpRight size={12} />
                </Link>
              </li>
              <li>
                <Link to="/budgets" className="hover:text-forest-500 transition-colors flex items-center gap-1">
                  Budgets <ArrowUpRight size={12} />
                </Link>
              </li>
              <li>
                <Link to="/analytics" className="hover:text-forest-500 transition-colors flex items-center gap-1">
                  Analytics <ArrowUpRight size={12} />
                </Link>
              </li>
            </ul>
          </div>

          {/* Tools & Info Column */}
          <div className="space-y-3">
            <p className="text-xs font-mono font-bold uppercase tracking-widest text-forest-500">
              Tools &amp; Info
            </p>
            <ul className="space-y-2 text-xs font-semibold uppercase tracking-wider text-ink-soft">
              <li>
                <Link to="/insights" className="hover:text-forest-500 transition-colors flex items-center gap-1">
                  AI Insights <ArrowUpRight size={12} />
                </Link>
              </li>
              <li>
                <Link to="/receipts" className="hover:text-forest-500 transition-colors flex items-center gap-1">
                  OCR Scanner <ArrowUpRight size={12} />
                </Link>
              </li>
              <li>
                <Link to="/export" className="hover:text-forest-500 transition-colors flex items-center gap-1">
                  Export Data <ArrowUpRight size={12} />
                </Link>
              </li>
              <li>
                <Link to="/about" className="hover:text-forest-500 transition-colors flex items-center gap-1">
                  About Ledger <ArrowUpRight size={12} />
                </Link>
              </li>
            </ul>
          </div>

          {/* Contact Support Column */}
          <div className="space-y-3">
            <p className="text-xs font-mono font-bold uppercase tracking-widest text-forest-500">
              Support &amp; Contact
            </p>
            <p className="text-xs text-ink-soft">Need assistance? Copy support address:</p>
            <button
              onClick={handleCopyContact}
              className="flex items-center gap-2 rounded-lg border border-mist-light/70 bg-paper px-3 py-2 text-xs font-mono text-ink hover:border-forest-500 transition-all duration-200"
            >
              <Mail size={14} className="text-forest-500" />
              <span>support@ledger.ai</span>
              {copied && <CheckCircle2 size={14} className="text-emerald-500 ml-auto" />}
            </button>
          </div>
        </div>

        {/* Footer Bottom Line */}
        <div className="mt-12 flex flex-col md:flex-row items-center justify-between gap-4 border-t border-mist-light/50 pt-6 text-xs font-mono text-mist">
          <div>
            © {new Date().getFullYear()} LEDGER. All rights reserved.
          </div>
          <button
            onClick={scrollToTop}
            className="flex items-center gap-1 rounded-full border border-mist-light/70 px-3 py-1 text-ink hover:border-forest-500 hover:text-forest-500 transition-all"
          >
            Back to Top <ChevronUp size={14} />
          </button>
        </div>
      </div>
    </footer>
  )
}
