import calendar
from datetime import date

from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.models.recurring_transaction import RecurringTransaction
from app.models.transaction import Transaction
from app.schemas.recurring_transaction import (
    RecurringTransactionCreate,
    RecurringTransactionUpdate,
)
from app.repositories.recurring_transaction_repository import RecurringTransactionRepository


class RecurringTransactionService:

    @staticmethod
    def create(db: Session, data: RecurringTransactionCreate, user_id: int):

        item = RecurringTransaction(
            description=data.description,
            amount=data.amount,
            type=data.type,
            category=data.category,
            notes=data.notes,
            day_of_month=data.day_of_month,
            user_id=user_id
        )

        return RecurringTransactionRepository.create(db, item)

    @staticmethod
    def get_all(db: Session, user_id: int):
        return RecurringTransactionRepository.get_all(db, user_id)

    @staticmethod
    def update(db: Session, item_id: int, data: RecurringTransactionUpdate, user_id: int):

        item = RecurringTransactionRepository.get_by_id(db, item_id, user_id)

        if item is None:
            raise HTTPException(status_code=404, detail="Recurring transaction not found")

        update_data = data.model_dump(exclude_unset=True)

        for field, value in update_data.items():
            setattr(item, field, value)

        return RecurringTransactionRepository.update(db, item)

    @staticmethod
    def delete(db: Session, item_id: int, user_id: int):

        item = RecurringTransactionRepository.get_by_id(db, item_id, user_id)

        if item is None:
            raise HTTPException(status_code=404, detail="Recurring transaction not found")

        RecurringTransactionRepository.delete(db, item)

        return {"message": "Recurring transaction deleted successfully"}

    @staticmethod
    def _is_due(item: RecurringTransaction, as_of: date) -> bool:

        if not item.is_active:
            return False

        if as_of.day < item.day_of_month:
            return False

        # Already generated for this calendar month?
        if item.last_run_date is not None:
            if (item.last_run_date.year, item.last_run_date.month) == (as_of.year, as_of.month):
                return False

        return True

    @staticmethod
    def _run_date_for(item: RecurringTransaction, as_of: date) -> date:

        last_day = calendar.monthrange(as_of.year, as_of.month)[1]
        day = min(item.day_of_month, last_day)

        return date(as_of.year, as_of.month, day)

    @staticmethod
    def generate_due_for_user(db: Session, user_id: int, as_of: date | None = None) -> list[Transaction]:
        """Generate any due recurring transactions for a single user. Safe
        to call repeatedly — already-generated months are skipped."""

        as_of = as_of or date.today()

        items = RecurringTransactionRepository.get_all(db, user_id)

        return RecurringTransactionService._generate(db, items, as_of)

    @staticmethod
    def generate_due_for_all_users(db: Session, as_of: date | None = None) -> list[Transaction]:
        """Used by the background scheduler — spans every user."""

        as_of = as_of or date.today()

        items = RecurringTransactionRepository.get_all_active(db)

        return RecurringTransactionService._generate(db, items, as_of)

    @staticmethod
    def _generate(db: Session, items: list[RecurringTransaction], as_of: date) -> list[Transaction]:

        created: list[Transaction] = []

        for item in items:

            if not RecurringTransactionService._is_due(item, as_of):
                continue

            txn = Transaction(
                date=RecurringTransactionService._run_date_for(item, as_of),
                description=item.description,
                amount=item.amount,
                type=item.type,
                category=item.category,
                notes=(item.notes or "") + " (auto-generated recurring transaction)",
                user_id=item.user_id
            )

            db.add(txn)
            item.last_run_date = as_of

            created.append(txn)

        if created:
            db.commit()

            for txn in created:
                db.refresh(txn)

        return created
