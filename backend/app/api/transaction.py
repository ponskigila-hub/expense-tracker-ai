from fastapi import APIRouter
from fastapi import Depends
from typing import List
from fastapi import HTTPException

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

@router.get(
    "/transactions",
    response_model=List[TransactionResponse]
)
def get_transactions(
    db: Session = Depends(get_db)
):
    transactions = db.query(Transaction).all()
    return transactions

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