from fastapi import APIRouter
from fastapi import Depends
from typing import List
from sqlalchemy.orm import Session

from app.database.database import get_db
from app.models.user import User
from app.security import get_current_user

from app.schemas.recurring_transaction import (
    RecurringTransactionCreate,
    RecurringTransactionUpdate,
    RecurringTransactionResponse,
)
from app.schemas.transaction import TransactionResponse
from app.services.recurring_transaction_service import RecurringTransactionService

router = APIRouter(
    tags=["Recurring Transactions"]
)


@router.post(
    "/recurring-transactions",
    response_model=RecurringTransactionResponse,
    status_code=201
)
def create_recurring(
    data: RecurringTransactionCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return RecurringTransactionService.create(db, data, current_user.id)


@router.get(
    "/recurring-transactions",
    response_model=List[RecurringTransactionResponse]
)
def list_recurring(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return RecurringTransactionService.get_all(db, current_user.id)


@router.put(
    "/recurring-transactions/{item_id}",
    response_model=RecurringTransactionResponse
)
def update_recurring(
    item_id: int,
    data: RecurringTransactionUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return RecurringTransactionService.update(db, item_id, data, current_user.id)


@router.delete("/recurring-transactions/{item_id}")
def delete_recurring(
    item_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return RecurringTransactionService.delete(db, item_id, current_user.id)


@router.post(
    "/recurring-transactions/run",
    response_model=List[TransactionResponse]
)
def run_recurring_now(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Manually trigger generation of any due recurring transactions for the
    current user. In production this also runs automatically once a day
    via a background scheduler (see app/scheduler.py) — this endpoint
    exists so it's testable/demoable on demand without waiting a day.
    """
    return RecurringTransactionService.generate_due_for_user(db, current_user.id)
