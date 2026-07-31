from sqlalchemy.orm import Session

from app.models.transaction import Transaction
from app.schemas.transaction import TransactionCreate
from app.repositories.transaction_repository import TransactionRepository

from fastapi import HTTPException


class TransactionService:

    @staticmethod
    def create_transaction(
        db: Session,
        transaction: TransactionCreate,
        user_id: int
    ):

        db_transaction = Transaction(
            date=transaction.date,
            description=transaction.description,
            amount=transaction.amount,
            type=transaction.type,
            category=transaction.category,
            notes=transaction.notes,
            user_id=user_id
        )

        return TransactionRepository.create(
            db,
            db_transaction
        )
    
    @staticmethod
    def get_transaction(
        db: Session,
        transaction_id: int,
        user_id: int
    ):

        transaction = TransactionRepository.get_by_id(
            db,
            transaction_id,
            user_id
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
        transaction_data: TransactionCreate,
        user_id: int
    ):

        transaction = TransactionRepository.get_by_id(
            db,
            transaction_id,
            user_id
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

        return TransactionRepository.update(
            db,
            transaction
        )
    
    @staticmethod
    def delete_transaction(
        db: Session,
        transaction_id: int,
        user_id: int
    ):

        transaction = TransactionRepository.get_by_id(
            db,
            transaction_id,
            user_id
        )

        if transaction is None:
            raise HTTPException(
                status_code=404,
                detail="Transaction not found"
            )

        TransactionRepository.delete(
            db,
            transaction
        )

        return {
            "message": "Transaction deleted successfully"
        }
        
    @staticmethod
    def get_transactions(
        db: Session,
        user_id: int
    ):
        return TransactionRepository.get_all(db, user_id)