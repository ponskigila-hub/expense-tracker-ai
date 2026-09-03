import json
from datetime import date, timedelta

import httpx
from sqlalchemy.orm import Session

from app.config import settings
from app.models.transaction import Transaction
from app.repositories.budget_repository import BudgetRepository
from app.repositories.transaction_repository import TransactionRepository
from app.services.insight_service import InsightService

# How many prior turns (from the client-supplied history) are replayed to
# the LLM. Keeps the prompt bounded even if a conversation runs long.
MAX_HISTORY_MESSAGES = 12

# How many of the user's most recent transactions are included as grounding
# context for the LLM. 60 is generous enough for "what did I spend this
# week" style questions without making the prompt unwieldy.
MAX_TRANSACTIONS_IN_CONTEXT = 60

FALLBACK_HELP_MESSAGE = (
    "I can answer things like \"how much did I spend on food this month\", "
    "\"what was my biggest expense last week\", \"how's my budget doing\", "
    "or \"am I spending more than usual\". Try rephrasing, or check the "
    "Insights and Analytics pages for a fuller picture."
)


def _fmt_rp(amount: float) -> str:
    """Format a number the way Rupiah amounts are usually written: a dot
    as the thousands separator and no decimals, e.g. 1234567 -> 'Rp1.234.567'."""

    return "Rp" + f"{amount:,.0f}".replace(",", ".")


class ChatService:

    # ---------------------------------------------------------------
    # Context building
    # ---------------------------------------------------------------

    @staticmethod
    def _recent_transactions(
        db: Session,
        user_id: int,
        limit: int = MAX_TRANSACTIONS_IN_CONTEXT,
    ) -> list[Transaction]:

        all_tx = TransactionRepository.get_all(db, user_id)
        all_tx.sort(key=lambda t: (t.date, t.created_at or t.date), reverse=True)

        return all_tx[:limit]

    @staticmethod
    def _budget_status(
        db: Session,
        user_id: int,
        current_by_category: dict[str, float],
    ) -> list[dict]:

        budgets = BudgetRepository.get_all(db, user_id)

        return [
            {
                "category": b.category,
                "budget": b.amount,
                "spent_this_month": current_by_category.get(b.category, 0.0),
            }
            for b in budgets
        ]

    @staticmethod
    def _biggest_expense(
        transactions: list[Transaction],
        days: int | None = None,
    ) -> Transaction | None:

        pool = [t for t in transactions if t.type == "expense"]

        if days is not None:
            cutoff = date.today() - timedelta(days=days)
            pool = [t for t in pool if t.date >= cutoff]

        return max(pool, key=lambda t: t.amount) if pool else None

    @staticmethod
    def build_context(db: Session, user_id: int) -> dict:

        stats = InsightService.compute_stats(db, user_id)
        transactions = ChatService._recent_transactions(db, user_id)
        budgets = ChatService._budget_status(db, user_id, stats["current_by_category"])

        return {
            "stats": stats,
            "transactions": transactions,
            "budgets": budgets,
        }

    # ---------------------------------------------------------------
    # LLM path
    # ---------------------------------------------------------------

    @staticmethod
    def _build_system_prompt(context: dict) -> str:

        stats = context["stats"]
        budgets = context["budgets"]

        tx_lines = [
            f"{t.date.isoformat()} | {t.type} | {t.category} | {t.amount} | {t.description}"
            for t in context["transactions"]
        ]

        return (
            "You are the AI financial assistant built into ExpenseTrackerAI, a "
            "personal expense-tracking app. All amounts are in Indonesian Rupiah "
            "(Rp). Answer the user's question about their own finances using "
            "ONLY the data provided below — never invent transactions, amounts, "
            "or dates that aren't present in it. If the data doesn't contain "
            "what's needed to answer, say so plainly and suggest where they "
            "could look instead (e.g. the Transactions or Analytics page). Keep "
            "replies short and conversational (1-4 sentences), plain text, no "
            "markdown, no bullet points. If the user asks something unrelated "
            "to their finances or this app, politely decline and steer the "
            "conversation back to their spending.\n\n"
            f"This month ({stats['this_month']}) expense by category: "
            f"{json.dumps(stats['current_by_category'])}\n"
            f"Last month ({stats['last_month']}) expense by category: "
            f"{json.dumps(stats['previous_by_category'])}\n"
            f"6-month category averages: {json.dumps(stats['category_averages'])}\n"
            f"This month total expense: {stats['current_total_expense']}\n"
            f"Last month total expense: {stats['previous_total_expense']}\n"
            f"This month income: {stats['current_income']}\n"
            f"Last month income: {stats['previous_income']}\n"
            f"Budgets (category, monthly budget, spent so far this month): "
            f"{json.dumps(budgets)}\n"
            "Most recent transactions (date | type | category | amount | "
            "description), newest first:\n" + "\n".join(tx_lines)
        )

    @staticmethod
    def generate_llm_reply(
        context: dict,
        message: str,
        history: list[dict],
    ) -> str | None:
        """
        Calls the Anthropic Messages API with the conversation plus grounding
        context. Returns None (never raises) on any failure — missing API
        key, network error, unexpected response shape — so the caller can
        fall back to the rule-based responder.
        """

        if not settings.ANTHROPIC_API_KEY:
            return None

        system_prompt = ChatService._build_system_prompt(context)

        messages = [
            {"role": turn["role"], "content": turn["content"]}
            for turn in history[-MAX_HISTORY_MESSAGES:]
        ]
        messages.append({"role": "user", "content": message})

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
                    "max_tokens": 400,
                    "system": system_prompt,
                    "messages": messages,
                },
                timeout=15.0,
            )

            response.raise_for_status()
            data = response.json()

            text_blocks = [
                block["text"]
                for block in data.get("content", [])
                if block.get("type") == "text"
            ]

            full_text = "\n".join(text_blocks).strip()

            return full_text or None

        except (httpx.HTTPError, KeyError, ValueError, TypeError):
            return None

    # ---------------------------------------------------------------
    # Rule-based fallback (zero-config path, no API key required)
    # ---------------------------------------------------------------

    @staticmethod
    def generate_rule_based_reply(context: dict, message: str) -> str:

        stats = context["stats"]
        budgets = context["budgets"]
        lowered = message.lower()

        known_categories = (
            set(stats["current_by_category"])
            | set(stats["previous_by_category"])
            | set(stats["category_averages"])
        )

        is_last_month = "last month" in lowered or "bulan lalu" in lowered
        period = "previous" if is_last_month else "current"
        period_label = "last month" if is_last_month else "this month"

        # 1. Biggest / largest expense
        if any(
            kw in lowered
            for kw in ["biggest expense", "largest expense", "most expensive", "pengeluaran terbesar"]
        ):
            days = None

            if any(kw in lowered for kw in ["last week", "past week", "minggu lalu"]):
                days = 7
            elif any(kw in lowered for kw in ["this month", "bulan ini"]):
                days = 30

            tx = ChatService._biggest_expense(context["transactions"], days=days)

            if not tx:
                return "I couldn't find any expenses in that period yet."

            return (
                f"Your biggest expense was {_fmt_rp(tx.amount)} on {tx.description} "
                f"({tx.category}) on {tx.date.strftime('%d %b %Y')}."
            )

        # 2. Category-specific spend
        matched_category = next(
            (c for c in known_categories if c.lower() in lowered), None
        )

        if matched_category and any(
            kw in lowered for kw in ["spend", "spent", "belanja", "pengeluaran"]
        ):
            by_cat = stats[f"{period}_by_category"]
            amount = by_cat.get(matched_category, 0.0)

            return f"You've spent {_fmt_rp(amount)} on {matched_category} {period_label}."

        # 3. Income
        if any(kw in lowered for kw in ["income", "pendapatan", "gaji"]):
            amount = stats[f"{period}_income"]

            return f"Your income {period_label} is {_fmt_rp(amount)}."

        # 4. Budget status
        if "budget" in lowered:
            if not budgets:
                return "You haven't set any budgets yet — head to the Budgets page to create one."

            lines = []

            for b in budgets[:5]:
                remaining = b["budget"] - b["spent_this_month"]
                status = "over" if remaining < 0 else "left"
                lines.append(
                    f"{b['category']}: {_fmt_rp(b['spent_this_month'])} of "
                    f"{_fmt_rp(b['budget'])} ({_fmt_rp(abs(remaining))} {status})"
                )

            return " | ".join(lines)

        # 5. "Am I spending more than usual" — reuse the insight engine
        if any(kw in lowered for kw in ["more than usual", "spending more", "biasa"]):
            insights = InsightService.generate_rule_based_insights(stats)
            return " ".join(insights[:2])

        # 6. Generic "how much did I spend" (no category)
        if "how much" in lowered and any(kw in lowered for kw in ["spend", "spent"]):
            amount = stats[f"{period}_total_expense"]
            return f"You've spent a total of {_fmt_rp(amount)} {period_label}."

        return FALLBACK_HELP_MESSAGE

    # ---------------------------------------------------------------
    # Orchestration
    # ---------------------------------------------------------------

    @staticmethod
    def get_reply(
        db: Session,
        user_id: int,
        message: str,
        history: list[dict],
    ) -> dict:

        context = ChatService.build_context(db, user_id)

        llm_reply = ChatService.generate_llm_reply(context, message, history)

        if llm_reply:
            return {"reply": llm_reply, "generated_by": "llm"}

        return {
            "reply": ChatService.generate_rule_based_reply(context, message),
            "generated_by": "rule_based",
        }
