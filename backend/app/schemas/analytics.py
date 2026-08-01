from pydantic import BaseModel
from typing import Literal


class DashboardResponse(BaseModel):

    balance: float

    income: float

    expense: float


class MonthlySummaryItem(BaseModel):

    month: str  # "2026-07"

    income: float

    expense: float

    balance: float


class CategorySummaryItem(BaseModel):

    category: str

    total: float

    percentage: float


class TrendPoint(BaseModel):

    label: str  # "2026-07-25" for daily buckets, "2026-07" for monthly buckets

    income: float

    expense: float


TrendPeriod = Literal["7d", "30d", "12m"]
