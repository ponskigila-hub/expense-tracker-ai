from sqlalchemy.orm import Session

from app.models.transaction import Transaction
from app.schemas.transaction import TransactionCreate

from fastapi import HTTPException

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
    
    @staticmethod
    def get_transaction(
        db: Session,
        transaction_id: int
    ):

        transaction = (
            db.query(Transaction)
            .filter(Transaction.id == transaction_id)
            .first()
        )

        if transaction is None:
            raise HTTPException(
                status_code=404,
                detail="Transaction not found"
            )

        return transaction
    
    @staticmethod
    def update_transaction(
        db: Session,
        transaction_id: int,
        transaction_data: TransactionCreate
    ):

        transaction = (
            db.query(Transaction)
            .filter(Transaction.id == transaction_id)
            .first()
        )

        if transaction is None:
            raise HTTPException(
                status_code=404,
                detail="Transaction not found"
            )

        transaction.date = transaction_data.date
        transaction.description = transaction_data.description
        transaction.amount = transaction_data.amount
        transaction.type = transaction_data.type
        transaction.category = transaction_data.category
        transaction.notes = transaction_data.notes

        db.commit()
        db.refresh(transaction)

        return transaction
    
    @staticmethod
    def delete_transaction(
        db: Session,
        transaction_id: int
    ):

        transaction = (
            db.query(Transaction)
            .filter(Transaction.id == transaction_id)
            .first()
        )

        if transaction is None:
            raise HTTPException(
                status_code=404,
                detail="Transaction not found"
            )

        db.delete(transaction)

        db.commit()

        return {
            "message": "Transaction deleted successfully"
        }
        
    @staticmethod
    def get_transactions(db: Session):
        return db.query(Transaction).all()