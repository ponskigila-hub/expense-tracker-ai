from sqlalchemy.orm import Session

from app.models.budget import Budget


class BudgetRepository:

    @staticmethod
    def create(
        db: Session,
        budget: Budget
    ):

        db.add(budget)

        db.commit()

        db.refresh(budget)

        return budget

    @staticmethod
    def get_all(
        db: Session,
        user_id: int
    ):

        return (
            db.query(Budget)
            .filter(Budget.user_id == user_id)
            .all()
        )

    @staticmethod
    def get_by_id(
        db: Session,
        budget_id: int,
        user_id: int
    ):

        return (
            db.query(Budget)
            .filter(
                Budget.id == budget_id,
                Budget.user_id == user_id
            )
            .first()
        )

    @staticmethod
    def get_by_category(
        db: Session,
        category: str,
        user_id: int
    ):

        return (
            db.query(Budget)
            .filter(
                Budget.category == category,
                Budget.user_id == user_id
            )
            .first()
        )

    @staticmethod
    def update(
        db: Session,
        budget: Budget
    ):

        db.commit()

        db.refresh(budget)

        return budget

    @staticmethod
    def delete(
        db: Session,
        budget: Budget
    ):

        db.delete(budget)

        db.commit()
