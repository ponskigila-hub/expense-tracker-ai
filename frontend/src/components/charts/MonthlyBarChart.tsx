import { BarChart, Bar, XAxis, YAxis, Tooltip, ResponsiveContainer, CartesianGrid, Legend } from 'recharts'
import type { MonthlySummaryItem } from '@/types'
import { formatMoney, formatMonthLabel } from '@/lib/format'
import { getChartPalette } from '@/lib/chartTheme'
import { useTheme } from '@/context/ThemeContext'

export function MonthlyBarChart({ data }: { data: MonthlySummaryItem[] }) {
  const { theme } = useTheme()
  const palette = getChartPalette(theme)
  const chartData = data.map((d) => ({ ...d, label: formatMonthLabel(d.month) }))

  return (
    <ResponsiveContainer width="100%" height={280}>
      <BarChart data={chartData} margin={{ top: 10, right: 12, left: 0, bottom: 0 }}>
        <CartesianGrid vertical={false} stroke={palette.grid} />
        <XAxis
          dataKey="label"
          tick={{ fontSize: 11, fill: palette.axisText }}
          axisLine={{ stroke: palette.grid }}
          tickLine={false}
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
        <Legend wrapperStyle={{ fontSize: 12, fontFamily: 'Inter, sans-serif', color: palette.tooltipText }} />
        <Bar dataKey="income" name="Income" fill={palette.income} radius={[4, 4, 0, 0]} maxBarSize={28} />
        <Bar dataKey="expense" name="Expense" fill={palette.expense} radius={[4, 4, 0, 0]} maxBarSize={28} />
      </BarChart>
    </ResponsiveContainer>
  )
}
