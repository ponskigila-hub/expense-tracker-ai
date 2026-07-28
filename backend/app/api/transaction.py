from fastapi import APIRouter
from fastapi import Depends
from typing import List
from fastapi import HTTPException
from app.services.transaction_service import TransactionService

from app.schemas.transaction import (
    TransactionCreate,
    TransactionResponse,
)
from sqlalchemy.orm import Session

from app.database.database import get_db

from app.models.transaction import Transaction

router = APIRouter()


@router.post(
    "/transactions",
    response_model=TransactionResponse
)

def create_transaction(
    transaction: TransactionCreate,
    db: Session = Depends(get_db)
):

    return TransactionService.create_transaction(
        db,
        transaction
    )

@router.get(
    "/transactions",
    response_model=List[TransactionResponse]
)
def get_transactions(
    db: Session = Depends(get_db)
):
    transactions = db.query(Transaction).all()
    return transactions


@router.put(
    "/transactions/{transaction_id}",
    response_model=TransactionResponse
)
def update_transaction(
    transaction_id: int,
    transaction: TransactionCreate,
    db: Session = Depends(get_db)
):

    db_transaction = (
        db.query(Transaction)
        .filter(Transaction.id == transaction_id)
        .first()
    )

    if db_transaction is None:
        raise HTTPException(
            status_code=404,
            detail="Transaction not found"
        )

    db_transaction.date = transaction.date
    db_transaction.description = transaction.description
    db_transaction.amount = transaction.amount
    db_transaction.type = transaction.type
    db_transaction.category = transaction.category
    db_transaction.notes = transaction.notes

    db.commit()

    db.refresh(db_transaction)

    return db_transaction

@router.delete("/transactions/{transaction_id}")
def delete_transaction(
    transaction_id: int,
    db: Session = Depends(get_db)
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

@router.get(
    "/transactions/{transaction_id}",
    response_model=TransactionResponse
)
def get_transaction(
    transaction_id: int,
    db: Session = Depends(get_db)
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