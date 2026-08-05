from fastapi import APIRouter
from fastapi import Depends
from fastapi import Query
from typing import Literal
from datetime import date
from app.services.transaction_service import TransactionService

from app.schemas.transaction import (
    TransactionCreate,
    TransactionResponse,
    PaginatedTransactionResponse,
)
from sqlalchemy.orm import Session

from app.database.database import get_db

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
    response_model=PaginatedTransactionResponse
)
def get_transactions(
    category: str | None = Query(default=None),
    type: str | None = Query(default=None, description="Filter by 'income' or 'expense'"),
    date_from: date | None = Query(default=None),
    date_to: date | None = Query(default=None),
    min_amount: float | None = Query(default=None, ge=0),
    max_amount: float | None = Query(default=None, ge=0),
    search: str | None = Query(default=None, description="Case-insensitive substring match on description"),
    sort_by: Literal["date", "amount", "description", "category", "created_at"] = Query(default="date"),
    sort_order: Literal["asc", "desc"] = Query(default="desc"),
    page: int = Query(default=1, ge=1),
    page_size: int = Query(default=20, ge=1, le=100),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return TransactionService.search_transactions(
        db,
        current_user.id,
        category=category,
        type_=type,
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
