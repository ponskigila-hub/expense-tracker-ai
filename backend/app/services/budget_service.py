from sqlalchemy.orm import Session
from sqlalchemy import func
from datetime import date

from fastapi import HTTPException

from app.models.budget import Budget
from app.models.transaction import Transaction
from app.schemas.budget import BudgetCreate, BudgetUpdate, BudgetResponse
from app.repositories.budget_repository import BudgetRepository


class BudgetService:

    @staticmethod
    def _spent_this_month(
        db: Session,
        user_id: int,
        category: str
    ) -> float:

        month_start = date.today().replace(day=1)

        total = (
            db.query(func.coalesce(func.sum(Transaction.amount), 0.0))
            .filter(
                Transaction.user_id == user_id,
                Transaction.category == category,
                Transaction.type == "expense",
                Transaction.date >= month_start
            )
            .scalar()
        )

        return float(total)

    @staticmethod
    def _to_response(
        db: Session,
        budget: Budget
    ) -> BudgetResponse:

        spent = BudgetService._spent_this_month(
            db,
            budget.user_id,
            budget.category
        )

        remaining = budget.amount - spent

        percentage_used = (
            round(spent / budget.amount * 100, 2)
            if budget.amount > 0 else 0.0
        )

        is_exceeded = spent > budget.amount

        warning = None

        if is_exceeded:
            warning = (
                f"You've exceeded your '{budget.category}' budget this month "
                f"by {spent - budget.amount:,.0f} "
                f"({percentage_used}% used)."
            )
        elif percentage_used >= 80:
            warning = (
                f"You've used {percentage_used}% of your '{budget.category}' "
                f"budget this month."
            )

        return BudgetResponse(
            id=budget.id,
            category=budget.category,
            amount=budget.amount,
            spent=spent,
            remaining=remaining,
            percentage_used=percentage_used,
            is_exceeded=is_exceeded,
            warning=warning,
            updated_at=budget.updated_at
        )

    @staticmethod
    def create_budget(
        db: Session,
        data: BudgetCreate,
        user_id: int
    ) -> BudgetResponse:

        existing = BudgetRepository.get_by_category(
            db,
            data.category,
            user_id
        )

        if existing:
            raise HTTPException(
                status_code=409,
                detail=(
                    f"A budget for '{data.category}' already exists. "
                    f"Use PUT /budget/{existing.id} to update it."
                )
            )

        budget = Budget(
            category=data.category,
            amount=data.amount,
            user_id=user_id
        )

        budget = BudgetRepository.create(db, budget)

        return BudgetService._to_response(db, budget)

    @staticmethod
    def get_budgets(
        db: Session,
        user_id: int
    ) -> list[BudgetResponse]:

        budgets = BudgetRepository.get_all(db, user_id)

        return [
            BudgetService._to_response(db, b)
            for b in budgets
        ]

    @staticmethod
    def update_budget(
        db: Session,
        budget_id: int,
        data: BudgetUpdate,
        user_id: int
    ) -> BudgetResponse:

        budget = BudgetRepository.get_by_id(db, budget_id, user_id)

        if budget is None:
            raise HTTPException(
                status_code=404,
                detail="Budget not found"
            )

        budget.amount = data.amount

        budget = BudgetRepository.update(db, budget)

        return BudgetService._to_response(db, budget)

    @staticmethod
    def delete_budget(
        db: Session,
        budget_id: int,
        user_id: int
    ):

        budget = BudgetRepository.get_by_id(db, budget_id, user_id)

        if budget is None:
            raise HTTPException(
                status_code=404,
                detail="Budget not found"
            )

        BudgetRepository.delete(db, budget)

        return {"message": "Budget deleted successfully"}
