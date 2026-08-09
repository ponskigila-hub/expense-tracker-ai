import { useState } from 'react'
import { Link } from 'react-router-dom'
import { ArrowUpRight, Github, Twitter, Linkedin, Mail, ShieldCheck, Sparkles, CheckCircle2, ChevronUp } from 'lucide-react'

export function Footer() {
  const [copied, setCopied] = useState(false)

  function handleCopyContact() {
    navigator.clipboard.writeText('support@expensetrackerai.com')
    setCopied(true)
    setTimeout(() => setCopied(false), 2000)
  }

  function scrollToTop() {
    window.scrollTo({ top: 0, behavior: 'smooth' })
  }

  return (
    <footer className="mt-20 border-t border-mist-light/50 bg-[#0A0B0F] text-ink relative overflow-hidden">
      {/* Interactive marquee header inspired by Coffee-Tech */}
      <div className="border-b border-mist-light/30 bg-[#0D0E13] py-6 overflow-hidden select-none">
        <div className="flex whitespace-nowrap animate-[marquee_25s_linear_infinite] gap-12 text-3xl md:text-5xl font-black font-display uppercase tracking-widest text-mist-light/30">
          <span>AI Financial Intelligence</span>
          <span className="text-forest-500">•</span>
          <span>Real-Time Telemetry</span>
          <span className="text-forest-500">•</span>
          <span>Automated OCR Receipt Audit</span>
          <span className="text-forest-500">•</span>
          <span>Precision Ledger</span>
          <span className="text-forest-500">•</span>
        </div>
      </div>

      <div className="mx-auto max-w-7xl px-6 py-16 md:px-8">
        <div className="grid gap-12 lg:grid-cols-5">
          {/* Brand Column */}
          <div className="lg:col-span-2 space-y-6">
            <div className="flex items-center gap-3">
              <div className="flex h-10 w-10 items-center justify-center rounded-xl bg-gradient-to-br from-forest-500 to-forest-700 shadow-[0_0_20px_rgba(200,96,61,0.5)] border border-forest-300/40">
                <div className="flex flex-col gap-[3.5px] items-center">
                  <span className="block h-[2.5px] w-5 rounded-full bg-ink" />
                  <span className="block h-[2.5px] w-3 rounded-full bg-brass-300" />
                  <span className="block h-[2.5px] w-5 rounded-full bg-forest-300" />
                </div>
              </div>
              <span className="font-display text-2xl font-black tracking-tight uppercase">
                COFFEE<span className="text-forest-500">TECH</span>
              </span>
            </div>
            <p className="text-sm text-ink-soft leading-relaxed max-w-md">
              ExpenseTrackerAI provides commercial-grade financial telemetry, OCR receipt analysis, and AI budget management for ambitious professionals.
            </p>
            <div className="flex items-center gap-3 text-xs font-mono text-mist uppercase tracking-widest pt-2">
              <span className="flex items-center gap-1.5 text-emerald-400">
                <ShieldCheck size={16} /> SOC2 Type II Certified
              </span>
              <span>•</span>
              <span className="flex items-center gap-1.5 text-forest-500">
                <Sparkles size={16} /> Gemini AI Powered
              </span>
            </div>
          </div>

          {/* Quick Links Column */}
          <div className="space-y-4">
            <p className="text-xs font-mono font-bold uppercase tracking-widest text-forest-500">
              Platform Features
            </p>
            <ul className="space-y-2.5 text-xs font-semibold uppercase tracking-wider text-ink-soft">
              <li>
                <Link to="/" className="hover:text-forest-300 transition-colors flex items-center gap-1">
                  Financial Dashboard <ArrowUpRight size={12} />
                </Link>
              </li>
              <li>
                <Link to="/transactions" className="hover:text-forest-300 transition-colors flex items-center gap-1">
                  Ledger Transactions <ArrowUpRight size={12} />
                </Link>
              </li>
              <li>
                <Link to="/budgets" className="hover:text-forest-300 transition-colors flex items-center gap-1">
                  Budget Allocations <ArrowUpRight size={12} />
                </Link>
              </li>
              <li>
                <Link to="/analytics" className="hover:text-forest-300 transition-colors flex items-center gap-1">
                  Telemetry Analytics <ArrowUpRight size={12} />
                </Link>
              </li>
            </ul>
          </div>

          {/* Tools Column */}
          <div className="space-y-4">
            <p className="text-xs font-mono font-bold uppercase tracking-widest text-forest-500">
              AI Tools &amp; Exports
            </p>
            <ul className="space-y-2.5 text-xs font-semibold uppercase tracking-wider text-ink-soft">
              <li>
                <Link to="/insights" className="hover:text-forest-300 transition-colors flex items-center gap-1">
                  AI Financial Insights <ArrowUpRight size={12} />
                </Link>
              </li>
              <li>
                <Link to="/receipts" className="hover:text-forest-300 transition-colors flex items-center gap-1">
                  OCR Receipt Scanner <ArrowUpRight size={12} />
                </Link>
              </li>
              <li>
                <Link to="/recurring" className="hover:text-forest-300 transition-colors flex items-center gap-1">
                  Recurring Expenses <ArrowUpRight size={12} />
                </Link>
              </li>
              <li>
                <Link to="/export" className="hover:text-forest-300 transition-colors flex items-center gap-1">
                  Data Export (CSV/JSON) <ArrowUpRight size={12} />
                </Link>
              </li>
            </ul>
          </div>

          {/* Interactive Contact & Socials Column */}
          <div className="space-y-4">
            <p className="text-xs font-mono font-bold uppercase tracking-widest text-forest-500">
              Interactive Connect
            </p>
            <p className="text-xs text-mist">Click to copy support email:</p>
            <button
              onClick={handleCopyContact}
              className="flex items-center gap-2 rounded-lg border border-mist-light/50 bg-surface px-3 py-2 text-xs font-mono text-ink hover:border-forest-500 transition-all duration-200"
            >
              <Mail size={14} className="text-forest-500" />
              <span>support@expensetrackerai.com</span>
              {copied && <CheckCircle2 size={14} className="text-emerald-400 ml-auto" />}
            </button>
            <div className="flex items-center gap-3 pt-2">
              <a
                href="https://github.com"
                target="_blank"
                rel="noreferrer"
                className="rounded-lg border border-mist-light/50 bg-surface p-2 text-ink-soft hover:text-forest-500 hover:border-forest-500 transition-colors"
              >
                <Github size={16} />
              </a>
              <a
                href="https://twitter.com"
                target="_blank"
                rel="noreferrer"
                className="rounded-lg border border-mist-light/50 bg-surface p-2 text-ink-soft hover:text-forest-500 hover:border-forest-500 transition-colors"
              >
                <Twitter size={16} />
              </a>
              <a
                href="https://linkedin.com"
                target="_blank"
                rel="noreferrer"
                className="rounded-lg border border-mist-light/50 bg-surface p-2 text-ink-soft hover:text-forest-500 hover:border-forest-500 transition-colors"
              >
                <Linkedin size={16} />
              </a>
            </div>
          </div>
        </div>

        {/* Footer Bottom Line */}
        <div className="mt-16 flex flex-col md:flex-row items-center justify-between gap-4 border-t border-mist-light/30 pt-8 text-xs font-mono text-mist">
          <div>
            © {new Date().getFullYear()} ExpenseTrackerAI. All rights reserved.
          </div>
          <div className="flex items-center gap-6">
            <span className="hover:text-ink cursor-pointer">Privacy Telemetry</span>
            <span>•</span>
            <span className="hover:text-ink cursor-pointer">Security Protocol</span>
            <span>•</span>
            <button
              onClick={scrollToTop}
              className="flex items-center gap-1 rounded-full border border-mist-light/50 px-3 py-1 text-ink hover:border-forest-500 hover:text-forest-500 transition-all"
            >
              Back to Top <ChevronUp size={14} />
            </button>
          </div>
        </div>
      </div>
    </footer>
  )
}
