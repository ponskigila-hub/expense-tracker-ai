from sqlalchemy.orm import Session

from app.models.transaction import Transaction
from app.schemas.transaction import TransactionCreate


class TransactionService:

    @staticmethod
    def create_transaction(
        db: Session,
        transaction: TransactionCreate
    ):

        db_transaction = Transaction(
            date=transaction.date,
            description=transaction.description,
            amount=transaction.amount,
            type=transaction.type,
            category=transaction.category,
            notes=transaction.notes
        )

        db.add(db_transaction)

        db.commit()

        db.refresh(db_transaction)

        return db_transaction