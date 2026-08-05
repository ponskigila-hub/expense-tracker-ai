from sqlalchemy.orm import Session
from sqlalchemy import func
from datetime import date
import json
import httpx

from app.models.transaction import Transaction
from app.config import settings


def _shift_month(d: date, months: int) -> date:
    """Return the 1st of the month `months` away from d's month (can be negative)."""

    month_index = d.month - 1 + months
    year = d.year + month_index // 12
    month = month_index % 12 + 1

    return date(year, month, 1)


class InsightService:

    @staticmethod
    def _category_totals(
        db: Session,
        user_id: int,
        month_start: date,
        month_end: date,
        type_: str = "expense"
    ) -> dict[str, float]:

        rows = (
            db.query(
                Transaction.category,
                func.sum(Transaction.amount).label("total")
            )
            .filter(
                Transaction.user_id == user_id,
                Transaction.type == type_,
                Transaction.date >= month_start,
                Transaction.date < month_end
            )
            .group_by(Transaction.category)
            .all()
        )

        return {category: float(total) for category, total in rows}

    @staticmethod
    def compute_stats(
        db: Session,
        user_id: int
    ) -> dict:

        this_month_start = date.today().replace(day=1)
        last_month_start = _shift_month(this_month_start, -1)

        current_by_category = InsightService._category_totals(
            db, user_id, this_month_start, _shift_month(this_month_start, 1)
        )
        previous_by_category = InsightService._category_totals(
            db, user_id, last_month_start, this_month_start
        )

        # Historical average per category, over the up-to-6 months before
        # the current (in-progress) month, so "above average" comparisons
        # aren't skewed by the current partial month.
        history_start = _shift_month(this_month_start, -6)

        history_rows = (
            db.query(
                Transaction.category,
                func.strftime("%Y-%m", Transaction.date).label("month"),
                func.sum(Transaction.amount).label("total")
            )
            .filter(
                Transaction.user_id == user_id,
                Transaction.type == "expense",
                Transaction.date >= history_start,
                Transaction.date < this_month_start
            )
            .group_by(Transaction.category, "month")
            .all()
        )

        per_category_months: dict[str, list[float]] = {}

        for category, _month, total in history_rows:
            per_category_months.setdefault(category, []).append(float(total))

        category_averages = {
            category: sum(totals) / len(totals)
            for category, totals in per_category_months.items()
        }

        current_income = sum(
            InsightService._category_totals(
                db, user_id, this_month_start, _shift_month(this_month_start, 1), "income"
            ).values()
        )
        previous_income = sum(
            InsightService._category_totals(
                db, user_id, last_month_start, this_month_start, "income"
            ).values()
        )

        return {
            "this_month": this_month_start.strftime("%Y-%m"),
            "last_month": last_month_start.strftime("%Y-%m"),
            "current_by_category": current_by_category,
            "previous_by_category": previous_by_category,
            "category_averages": category_averages,
            "current_total_expense": sum(current_by_category.values()),
            "previous_total_expense": sum(previous_by_category.values()),
            "current_income": current_income,
            "previous_income": previous_income,
            "has_enough_history": len(history_rows) > 0 or len(previous_by_category) > 0,
        }

    @staticmethod
    def _pct_change(old: float, new: float) -> float | None:

        if old <= 0:
            return None

        return round((new - old) / old * 100, 1)

    @staticmethod
    def generate_rule_based_insights(stats: dict) -> list[str]:

        insights: list[str] = []

        current_cat = stats["current_by_category"]
        previous_cat = stats["previous_by_category"]
        averages = stats["category_averages"]

        changes = []

        for category, current_amount in current_cat.items():
            previous_amount = previous_cat.get(category, 0.0)
            pct = InsightService._pct_change(previous_amount, current_amount)

            if pct is not None:
                changes.append((category, pct, current_amount))

        changes.sort(key=lambda x: x[1], reverse=True)

        # Biggest increase
        if changes and changes[0][1] >= 15:
            category, pct, _ = changes[0]
            insights.append(
                f"Your spending on {category} increased by {pct}% compared to last month."
            )

        # Biggest decrease
        drops = [c for c in changes if c[1] <= -15]

        if drops:
            category, pct, _ = min(drops, key=lambda x: x[1])
            insights.append(
                f"Nice — your spending on {category} dropped by {abs(pct)}% compared to last month."
            )

        # Categories currently trending above their own historical average
        for category, current_amount in current_cat.items():
            avg = averages.get(category)

            if avg and avg > 0 and current_amount > avg * 1.2:
                over_pct = round((current_amount - avg) / avg * 100, 1)
                insights.append(
                    f"{category} spending is {over_pct}% above your usual monthly average."
                )

        # Overall picture
        total_pct = InsightService._pct_change(
            stats["previous_total_expense"],
            stats["current_total_expense"]
        )

        if total_pct is not None and abs(total_pct) >= 10:
            direction = "more" if total_pct > 0 else "less"
            insights.append(
                f"Overall, you've spent {abs(total_pct)}% {direction} this month than last month."
            )

        if not stats["has_enough_history"]:
            insights.append(
                "Not enough transaction history yet for month-over-month comparisons — "
                "keep logging transactions and insights will get sharper."
            )

        if not insights:
            insights.append(
                "Your spending this month looks steady compared to last month — no major changes detected."
            )

        return insights[:5]

    @staticmethod
    def _build_prompt(stats: dict) -> str:

        return (
            "You are a personal finance assistant. Based on the following "
            "aggregated monthly spending data (in Indonesian Rupiah), write "
            "2-4 short, specific, encouraging insight sentences a user would "
            "see on their finance dashboard. Mention concrete categories and "
            "percentage changes where relevant. Do not invent numbers that "
            "aren't in the data. Return each insight as a separate line, no "
            "numbering, no markdown.\n\n"
            f"This month ({stats['this_month']}) expense by category: "
            f"{json.dumps(stats['current_by_category'])}\n"
            f"Last month ({stats['last_month']}) expense by category: "
            f"{json.dumps(stats['previous_by_category'])}\n"
            f"6-month category averages: {json.dumps(stats['category_averages'])}\n"
            f"This month total expense: {stats['current_total_expense']}\n"
            f"Last month total expense: {stats['previous_total_expense']}\n"
            f"This month income: {stats['current_income']}\n"
            f"Last month income: {stats['previous_income']}\n"
        )

    @staticmethod
    def generate_llm_insights(stats: dict) -> list[str] | None:
        """
        Calls the Anthropic Messages API to turn the stats into natural
        language insights. Returns None (never raises) on any failure —
        missing API key, network error, unexpected response shape — so
        the caller can fall back to the rule-based generator. This means
        the endpoint works with zero configuration, and gets an upgrade
        automatically if ANTHROPIC_API_KEY is set in .env.
        """

        if not settings.ANTHROPIC_API_KEY:
            return None

        prompt = InsightService._build_prompt(stats)

        try:
            response = httpx.post(
                "https://api.anthropic.com/v1/messages",
                headers={
                    "x-api-key": settings.ANTHROPIC_API_KEY,
                    "anthropic-version": "2023-06-01",
                    "content-type": "application/json",
                },
                json={
                    "model": settings.ANTHROPIC_MODEL,
                    "max_tokens": 300,
                    "messages": [
                        {"role": "user", "content": prompt}
                    ],
                },
                timeout=10.0,
            )

            response.raise_for_status()
            data = response.json()

            text_blocks = [
                block["text"]
                for block in data.get("content", [])
                if block.get("type") == "text"
            ]

            full_text = "\n".join(text_blocks).strip()

            if not full_text:
                return None

            lines = [
                line.strip("-• ").strip()
                for line in full_text.splitlines()
                if line.strip()
            ]

            return lines[:5] if lines else None

        except (httpx.HTTPError, KeyError, ValueError, TypeError):
            return None

    @staticmethod
    def get_insights(
        db: Session,
        user_id: int
    ) -> dict:

        stats = InsightService.compute_stats(db, user_id)

        llm_insights = InsightService.generate_llm_insights(stats)

        if llm_insights:
            return {
                "insights": llm_insights,
                "generated_by": "llm",
                "stats": stats,
            }

        return {
            "insights": InsightService.generate_rule_based_insights(stats),
            "generated_by": "rule_based",
            "stats": stats,
        }
