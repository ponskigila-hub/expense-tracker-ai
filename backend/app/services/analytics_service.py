from sqlalchemy.orm import Session
from sqlalchemy import func
from datetime import date, timedelta

from app.models.transaction import Transaction
from app.schemas.analytics import (
    DashboardResponse,
    MonthlySummaryItem,
    CategorySummaryItem,
    TrendPoint,
)
from app.utils.db_helpers import month_expr


class AnalyticsService:

    @staticmethod
    def _sum(db: Session, user_id: int, type_: str) -> float:

        total = (
            db.query(func.coalesce(func.sum(Transaction.amount), 0.0))
            .filter(
                Transaction.user_id == user_id,
                Transaction.type == type_
            )
            .scalar()
        )

        return float(total)

    @staticmethod
    def get_dashboard(
        db: Session,
        user_id: int
    ) -> DashboardResponse:

        income = AnalyticsService._sum(db, user_id, "income")
        expense = AnalyticsService._sum(db, user_id, "expense")

        return DashboardResponse(
            balance=income - expense,
            income=income,
            expense=expense
        )

    @staticmethod
    def get_monthly_summary(
        db: Session,
        user_id: int
    ) -> list[MonthlySummaryItem]:

        month_expr_ = month_expr(db, Transaction.date)

        rows = (
            db.query(
                month_expr_.label("month"),
                Transaction.type,
                func.sum(Transaction.amount).label("total")
            )
            .filter(Transaction.user_id == user_id)
            .group_by(month_expr_, Transaction.type)
            .order_by(month_expr_)
            .all()
        )

        by_month: dict[str, dict[str, float]] = {}

        for month, txn_type, total in rows:
            by_month.setdefault(month, {"income": 0.0, "expense": 0.0})
            by_month[month][txn_type] = float(total)

        return [
            MonthlySummaryItem(
                month=month,
                income=values["income"],
                expense=values["expense"],
                balance=values["income"] - values["expense"]
            )
            for month, values in sorted(by_month.items())
        ]

    @staticmethod
    def get_category_summary(
        db: Session,
        user_id: int
    ) -> list[CategorySummaryItem]:

        rows = (
            db.query(
                Transaction.category,
                func.sum(Transaction.amount).label("total")
            )
            .filter(
                Transaction.user_id == user_id,
                Transaction.type == "expense"
            )
            .group_by(Transaction.category)
            .order_by(func.sum(Transaction.amount).desc())
            .all()
        )

        grand_total = sum(float(total) for _, total in rows)

        return [
            CategorySummaryItem(
                category=category,
                total=float(total),
                percentage=(
                    round(float(total) / grand_total * 100, 2)
                    if grand_total > 0 else 0.0
                )
            )
            for category, total in rows
        ]

    @staticmethod
    def get_trend(
        db: Session,
        user_id: int,
        period: str
    ) -> list[TrendPoint]:

        if period == "7d":
            return AnalyticsService._daily_trend(db, user_id, days=7)

        if period == "30d":
            return AnalyticsService._daily_trend(db, user_id, days=30)

        if period == "12m":
            return AnalyticsService._monthly_trend(db, user_id, months=12)

        raise ValueError(f"Unsupported trend period: {period}")

    @staticmethod
    def _daily_trend(
        db: Session,
        user_id: int,
        days: int
    ) -> list[TrendPoint]:

        start_date = date.today() - timedelta(days=days - 1)

        rows = (
            db.query(
                Transaction.date,
                Transaction.type,
                func.sum(Transaction.amount).label("total")
            )
            .filter(
                Transaction.user_id == user_id,
                Transaction.date >= start_date
            )
            .group_by(Transaction.date, Transaction.type)
            .all()
        )

        by_day: dict[str, dict[str, float]] = {}

        for txn_date, txn_type, total in rows:
            key = txn_date.isoformat()
            by_day.setdefault(key, {"income": 0.0, "expense": 0.0})
            by_day[key][txn_type] = float(total)

        # Build a continuous series so days with no transactions show as 0,
        # rather than being missing from the chart entirely.
        points = []

        for i in range(days):
            d = start_date + timedelta(days=i)
            key = d.isoformat()
            values = by_day.get(key, {"income": 0.0, "expense": 0.0})

            points.append(
                TrendPoint(
                    label=key,
                    income=values["income"],
                    expense=values["expense"]
                )
            )

        return points

    @staticmethod
    def _monthly_trend(
        db: Session,
        user_id: int,
        months: int
    ) -> list[TrendPoint]:

        month_expr_ = month_expr(db, Transaction.date)

        # Compute the earliest month boundary (approx, using 31-day steps
        # then normalizing to the 1st) so the SQL side can filter cheaply.
        cutoff = date.today().replace(day=1)

        for _ in range(months - 1):
            cutoff = (cutoff - timedelta(days=1)).replace(day=1)

        rows = (
            db.query(
                month_expr_.label("month"),
                Transaction.type,
                func.sum(Transaction.amount).label("total")
            )
            .filter(
                Transaction.user_id == user_id,
                Transaction.date >= cutoff
            )
            .group_by(month_expr_, Transaction.type)
            .all()
        )

        by_month: dict[str, dict[str, float]] = {}

        for month, txn_type, total in rows:
            by_month.setdefault(month, {"income": 0.0, "expense": 0.0})
            by_month[month][txn_type] = float(total)

        # Build continuous month series, oldest -> newest.
        points = []
        cursor = cutoff

        for _ in range(months):
            key = cursor.strftime("%Y-%m")
            values = by_month.get(key, {"income": 0.0, "expense": 0.0})

            points.append(
                TrendPoint(
                    label=key,
                    income=values["income"],
                    expense=values["expense"]
                )
            )

            # advance to next month
            next_month = (cursor.replace(day=28) + timedelta(days=4)).replace(day=1)
            cursor = next_month

        return points
