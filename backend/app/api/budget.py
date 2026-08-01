from fastapi import APIRouter
from fastapi import Depends
from typing import List
from sqlalchemy.orm import Session

from app.database.database import get_db
from app.models.user import User
from app.security import get_current_user

from app.schemas.budget import BudgetCreate, BudgetUpdate, BudgetResponse
from app.services.budget_service import BudgetService

router = APIRouter(
    tags=["Budget"]
)


@router.post(
    "/budget",
    response_model=BudgetResponse,
    status_code=201
)
def create_budget(
    budget: BudgetCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return BudgetService.create_budget(db, budget, current_user.id)


@router.get(
    "/budget",
    response_model=List[BudgetResponse]
)
def get_budgets(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return BudgetService.get_budgets(db, current_user.id)


@router.put(
    "/budget/{budget_id}",
    response_model=BudgetResponse
)
def update_budget(
    budget_id: int,
    budget: BudgetUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return BudgetService.update_budget(db, budget_id, budget, current_user.id)


@router.delete("/budget/{budget_id}")
def delete_budget(
    budget_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return BudgetService.delete_budget(db, budget_id, current_user.id)
