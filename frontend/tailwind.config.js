/** @type {import('tailwindcss').Config} */
export default {
  darkMode: 'class',
  content: ['./index.html', './src/**/*.{js,ts,jsx,tsx}'],
  theme: {
    extend: {
      colors: {
        // "Ledger" palette — driven by CSS variables (see src/index.css) so
        // every token below automatically resolves to its light or dark
        // value depending on whether <html> has the `dark` class. The
        // `rgb(var(...) / <alpha-value>)` form is what lets Tailwind's
        // opacity modifiers (e.g. bg-ink/40) keep working with variables.
        paper: {
          DEFAULT: 'rgb(var(--color-paper) / <alpha-value>)',
          dim: 'rgb(var(--color-paper-dim) / <alpha-value>)',
        },
        surface: 'rgb(var(--color-surface) / <alpha-value>)',
        ink: {
          DEFAULT: 'rgb(var(--color-ink) / <alpha-value>)',
          soft: 'rgb(var(--color-ink-soft) / <alpha-value>)',
        },
        mist: {
          DEFAULT: 'rgb(var(--color-mist) / <alpha-value>)',
          light: 'rgb(var(--color-mist-light) / <alpha-value>)',
        },
        forest: {
          50: 'rgb(var(--color-forest-50) / <alpha-value>)',
          100: 'rgb(var(--color-forest-100) / <alpha-value>)',
          300: 'rgb(var(--color-forest-300) / <alpha-value>)',
          500: 'rgb(var(--color-forest-500) / <alpha-value>)',
          600: 'rgb(var(--color-forest-600) / <alpha-value>)',
          700: 'rgb(var(--color-forest-700) / <alpha-value>)',
        },
        brass: {
          100: 'rgb(var(--color-brass-100) / <alpha-value>)',
          300: 'rgb(var(--color-brass-300) / <alpha-value>)',
          500: 'rgb(var(--color-brass-500) / <alpha-value>)',
          600: 'rgb(var(--color-brass-600) / <alpha-value>)',
        },
        rust: {
          100: 'rgb(var(--color-rust-100) / <alpha-value>)',
          300: 'rgb(var(--color-rust-300) / <alpha-value>)',
          500: 'rgb(var(--color-rust-500) / <alpha-value>)',
          600: 'rgb(var(--color-rust-600) / <alpha-value>)',
        },
      },
      fontFamily: {
        display: ['"Fraunces"', 'ui-serif', 'Georgia', 'serif'],
        sans: ['"Inter"', 'ui-sans-serif', 'system-ui', 'sans-serif'],
        mono: ['"IBM Plex Mono"', 'ui-monospace', 'SFMono-Regular', 'monospace'],
      },
      borderRadius: { sm: '6px', DEFAULT: '10px', lg: '14px' },
      boxShadow: {
        card: '0 1px 2px rgb(var(--color-ink) / 0.04), 0 1px 12px rgb(var(--color-ink) / 0.04)',
        pop: '0 8px 28px rgb(var(--color-ink) / 0.16)',
      },
    },
  },
  plugins: [],
}
