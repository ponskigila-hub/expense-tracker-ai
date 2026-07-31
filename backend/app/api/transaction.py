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
from app.models.user import User
from app.security import get_current_user

router = APIRouter(
    tags=["Transactions"]
)

@router.post(
    "/transactions",
    response_model=TransactionResponse
)

def create_transaction(
    transaction: TransactionCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    return TransactionService.create_transaction(
        db,
        transaction,
        current_user.id
    )

@router.get(
    "/transactions",
    response_model=List[TransactionResponse]
)
def get_transactions(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return TransactionService.get_transactions(
        db,
        current_user.id
    )


@router.put(
    "/transactions/{transaction_id}",
    response_model=TransactionResponse
)   
def update_transaction(
    transaction_id: int,
    transaction: TransactionCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    return TransactionService.update_transaction(
        db,
        transaction_id,
        transaction,
        current_user.id
    )

@router.delete("/transactions/{transaction_id}")
def delete_transaction(
    transaction_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return TransactionService.delete_transaction(
        db,
        transaction_id,
        current_user.id
    )

@router.get(
    "/transactions/{transaction_id}",
    response_model=TransactionResponse
)
def get_transaction(
    transaction_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    return TransactionService.get_transaction(
        db,
        transaction_id,
        current_user.id
    )
