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
    def search_transactions(
        db: Session,
        user_id: int,
        category: str | None = None,
        type_: str | None = None,
        date_from=None,
        date_to=None,
        min_amount: float | None = None,
        max_amount: float | None = None,
        search: str | None = None,
        sort_by: str = "date",
        sort_order: str = "desc",
        page: int = 1,
        page_size: int = 20,
    ):

        items, total = TransactionRepository.search(
            db,
            user_id,
            category=category,
            type_=type_,
            date_from=date_from,
            date_to=date_to,
            min_amount=min_amount,
            max_amount=max_amount,
            search=search,
            sort_by=sort_by,
            sort_order=sort_order,
            page=page,
            page_size=page_size,
        )

        total_pages = (total + page_size - 1) // page_size if page_size > 0 else 0

        return {
            "items": items,
            "total": total,
            "page": page,
            "page_size": page_size,
            "total_pages": total_pages,
        }