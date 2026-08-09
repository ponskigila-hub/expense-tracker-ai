import { PieChart, Pie, Cell, ResponsiveContainer, Tooltip } from 'recharts'
import type { CategorySummaryItem } from '@/types'
import { colorForCategory, formatMoney } from '@/lib/format'
import { getChartPalette } from '@/lib/chartTheme'
import { useTheme } from '@/context/ThemeContext'
import { EmptyState } from '@/components/ui/Misc'
import { PieChart as PieIcon } from 'lucide-react'

export function CategoryDonut({ data }: { data: CategorySummaryItem[] }) {
  const { theme } = useTheme()
  const palette = getChartPalette(theme)

  if (!data.length) {
    return (
      <EmptyState
        icon={<PieIcon size={28} />}
        title="No spending yet"
        description="Add a transaction to see your category breakdown."
      />
    )
  }

  return (
    <div className="flex flex-col items-center gap-4 sm:flex-row sm:items-center">
      <div className="h-52 w-52 shrink-0">
        <ResponsiveContainer width="100%" height="100%">
          <PieChart>
            <Pie
              data={data}
              dataKey="total"
              nameKey="category"
              innerRadius="62%"
              outerRadius="95%"
              paddingAngle={2}
              stroke="none"
            >
              {data.map((entry) => (
                <Cell key={entry.category} fill={colorForCategory(entry.category)} />
              ))}
            </Pie>
            <Tooltip
              formatter={(value: number) => formatMoney(value)}
              contentStyle={{
                borderRadius: 10,
                border: `1px solid ${palette.tooltipBorder}`,
                background: palette.tooltipBg,
                fontSize: 12,
                fontFamily: 'Inter, sans-serif',
              }}
              labelStyle={{ color: palette.tooltipText }}
            />
          </PieChart>
        </ResponsiveContainer>
      </div>
      <ul className="w-full flex-1 space-y-2.5">
        {data.map((item) => (
          <li key={item.category} className="flex items-center gap-2.5 text-sm">
            <span
              className="h-2.5 w-2.5 shrink-0 rounded-full"
              style={{ backgroundColor: colorForCategory(item.category) }}
            />
            <span className="flex-1 truncate capitalize text-ink-soft">{item.category}</span>
            <span className="font-mono text-xs text-mist">{item.percentage.toFixed(0)}%</span>
            <span className="w-20 text-right font-mono tabular text-ink">
              {formatMoney(item.total)}
            </span>
          </li>
        ))}
      </ul>
    </div>
  )
}
