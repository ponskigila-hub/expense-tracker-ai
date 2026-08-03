import datetime

import pytest
from fastapi import HTTPException

from app.models.user import User
from app.models.transaction import Transaction
from app.schemas.budget import BudgetCreate, BudgetUpdate
from app.services.budget_service import BudgetService
from app.security import pwd_context


def _make_user(db_session, email="budget_svc@test.com") -> User:

    user = User(
        username=email.split("@")[0],
        email=email,
        hashed_password=pwd_context.hash("password123")
    )
    db_session.add(user)
    db_session.commit()
    db_session.refresh(user)

    return user


def _spend(db_session, user_id, category, amount):

    db_session.add(Transaction(
        date=datetime.date.today(), description="spend", amount=amount,
        type="expense", category=category, user_id=user_id
    ))
    db_session.commit()


def test_create_budget_rejects_duplicate_category(db_session):

    user = _make_user(db_session)

    BudgetService.create_budget(db_session, BudgetCreate(category="Food", amount=100000), user.id)

    with pytest.raises(HTTPException) as exc_info:
        BudgetService.create_budget(db_session, BudgetCreate(category="Food", amount=200000), user.id)

    assert exc_info.value.status_code == 409


def test_budget_warning_thresholds(db_session):

    user = _make_user(db_session)
    BudgetService.create_budget(db_session, BudgetCreate(category="Food", amount=100000), user.id)

    # Under 80% -> no warning
    _spend(db_session, user.id, "Food", 50000)
    result = BudgetService.get_budgets(db_session, user.id)[0]
    assert result.warning is None
    assert result.is_exceeded is False

    # >=80% -> warning, not yet exceeded
    _spend(db_session, user.id, "Food", 35000)  # total 85000 = 85%
    result = BudgetService.get_budgets(db_session, user.id)[0]
    assert result.warning is not None
    assert result.is_exceeded is False

    # Over 100% -> exceeded
    _spend(db_session, user.id, "Food", 30000)  # total 115000 = 115%
    result = BudgetService.get_budgets(db_session, user.id)[0]
    assert result.is_exceeded is True
    assert "exceeded" in result.warning.lower()


def test_update_budget_not_found_raises_404(db_session):

    user = _make_user(db_session)

    with pytest.raises(HTTPException) as exc_info:
        BudgetService.update_budget(db_session, 999, BudgetUpdate(amount=1), user.id)

    assert exc_info.value.status_code == 404


def test_check_and_send_alerts_is_idempotent_per_month(db_session):

    user = _make_user(db_session)
    BudgetService.create_budget(db_session, BudgetCreate(category="Food", amount=100000), user.id)
    _spend(db_session, user.id, "Food", 95000)

    first_run = BudgetService.check_and_send_alerts(db_session)
    assert len(first_run) == 1

    second_run = BudgetService.check_and_send_alerts(db_session)
    assert len(second_run) == 0  # already alerted this month
