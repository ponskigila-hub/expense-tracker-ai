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
    return TransactionService.get_transactions(db)


@router.put(
    "/transactions/{transaction_id}",
    response_model=TransactionResponse
)
def update_transaction(
    transaction_id: int,
    transaction: TransactionCreate,
    db: Session = Depends(get_db)
):

    return TransactionService.update_transaction(
        db,
        transaction_id,
        transaction
    )

@router.delete("/transactions/{transaction_id}")
def delete_transaction(
    transaction_id: int,
    db: Session = Depends(get_db)
):
    return TransactionService.delete_transaction(
        db,
        transaction_id
    )

@router.get(
    "/transactions/{transaction_id}",
    response_model=TransactionResponse
)
def get_transaction(
    transaction_id: int,
    db: Session = Depends(get_db)
):

    return TransactionService.get_transaction(
        db,
        transaction_id
    )