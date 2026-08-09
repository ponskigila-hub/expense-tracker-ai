// recharts renders via inline SVG attributes/JS style objects, which can't
// read our CSS custom properties directly — so chart-specific colors are
// kept here as plain hex, switched explicitly based on the active theme.

export interface ChartPalette {
  grid: string
  axisText: string
  tooltipBg: string
  tooltipBorder: string
  tooltipText: string
  income: string
  expense: string
}

const light: ChartPalette = {
  grid: '#D8DDD7',
  axisText: '#8B948E',
  tooltipBg: '#FFFFFF',
  tooltipBorder: '#D8DDD7',
  tooltipText: '#16231F',
  income: '#1F5C4C',
  expense: '#A6432F',
}

const dark: ChartPalette = {
  grid: '#2C3B35',
  axisText: '#828F87',
  tooltipBg: '#1B2522',
  tooltipBorder: '#2F3C37',
  tooltipText: '#ECF0EC',
  income: '#3E9478',
  expense: '#D86C57',
}

export function getChartPalette(theme: 'light' | 'dark'): ChartPalette {
  return theme === 'dark' ? dark : light
}
