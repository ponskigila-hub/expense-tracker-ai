from sqlalchemy.orm import Session

from app.models.recurring_transaction import RecurringTransaction


class RecurringTransactionRepository:

    @staticmethod
    def create(db: Session, item: RecurringTransaction):
        db.add(item)
        db.commit()
        db.refresh(item)
        return item

    @staticmethod
    def get_all(db: Session, user_id: int):
        return (
            db.query(RecurringTransaction)
            .filter(RecurringTransaction.user_id == user_id)
            .all()
        )

    @staticmethod
    def get_by_id(db: Session, item_id: int, user_id: int):
        return (
            db.query(RecurringTransaction)
            .filter(
                RecurringTransaction.id == item_id,
                RecurringTransaction.user_id == user_id
            )
            .first()
        )

    @staticmethod
    def get_all_active(db: Session):
        """Used by the scheduler — spans all users."""
        return (
            db.query(RecurringTransaction)
            .filter(RecurringTransaction.is_active == True)  # noqa: E712
            .all()
        )

    @staticmethod
    def update(db: Session, item: RecurringTransaction):
        db.commit()
        db.refresh(item)
        return item

    @staticmethod
    def delete(db: Session, item: RecurringTransaction):
        db.delete(item)
        db.commit()
