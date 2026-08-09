import {
  AreaChart,
  Area,
  XAxis,
  YAxis,
  Tooltip,
  ResponsiveContainer,
  CartesianGrid,
} from 'recharts'
import type { TrendPoint } from '@/types'
import { formatMoney } from '@/lib/format'
import { getChartPalette } from '@/lib/chartTheme'
import { useTheme } from '@/context/ThemeContext'

export function TrendChart({ data }: { data: TrendPoint[] }) {
  const { theme } = useTheme()
  const palette = getChartPalette(theme)

  return (
    <ResponsiveContainer width="100%" height={260}>
      <AreaChart data={data} margin={{ top: 10, right: 12, left: 0, bottom: 0 }}>
        <defs>
          <linearGradient id="incomeFill" x1="0" y1="0" x2="0" y2="1">
            <stop offset="0%" stopColor={palette.income} stopOpacity={0.28} />
            <stop offset="100%" stopColor={palette.income} stopOpacity={0} />
          </linearGradient>
          <linearGradient id="expenseFill" x1="0" y1="0" x2="0" y2="1">
            <stop offset="0%" stopColor={palette.expense} stopOpacity={0.22} />
            <stop offset="100%" stopColor={palette.expense} stopOpacity={0} />
          </linearGradient>
        </defs>
        <CartesianGrid vertical={false} stroke={palette.grid} />
        <XAxis
          dataKey="label"
          tick={{ fontSize: 11, fill: palette.axisText }}
          axisLine={{ stroke: palette.grid }}
          tickLine={false}
          minTickGap={24}
        />
        <YAxis
          tick={{ fontSize: 11, fill: palette.axisText }}
          axisLine={false}
          tickLine={false}
          width={56}
          tickFormatter={(v) => `$${v >= 1000 ? `${(v / 1000).toFixed(1)}k` : v}`}
        />
        <Tooltip
          formatter={(value: number) => formatMoney(value)}
          contentStyle={{
            borderRadius: 10,
            border: `1px solid ${palette.tooltipBorder}`,
            background: palette.tooltipBg,
            fontSize: 12,
            fontFamily: 'Inter, sans-serif',
          }}
          labelStyle={{ color: palette.tooltipText, fontWeight: 600 }}
        />
        <Area
          type="monotone"
          dataKey="income"
          stroke={palette.income}
          strokeWidth={2}
          fill="url(#incomeFill)"
          name="Income"
        />
        <Area
          type="monotone"
          dataKey="expense"
          stroke={palette.expense}
          strokeWidth={2}
          fill="url(#expenseFill)"
          name="Expense"
        />
      </AreaChart>
    </ResponsiveContainer>
  )
}
