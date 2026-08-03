import datetime

from app.models.user import User
from app.models.recurring_transaction import RecurringTransaction
from app.services.recurring_transaction_service import RecurringTransactionService
from app.security import pwd_context


def _make_user(db_session, email="recurring_svc@test.com") -> User:

    user = User(
        username=email.split("@")[0],
        email=email,
        hashed_password=pwd_context.hash("password123")
    )
    db_session.add(user)
    db_session.commit()
    db_session.refresh(user)

    return user


def test_not_due_before_day_of_month(db_session):

    user = _make_user(db_session)
    item = RecurringTransaction(
        description="Netflix", amount=150000, type="expense",
        category="Subscription", day_of_month=12, user_id=user.id
    )
    db_session.add(item)
    db_session.commit()

    generated = RecurringTransactionService.generate_due_for_user(
        db_session, user.id, as_of=datetime.date(2026, 8, 10)
    )
    assert generated == []


def test_generates_once_due_then_idempotent_same_month(db_session):

    user = _make_user(db_session)
    item = RecurringTransaction(
        description="Netflix", amount=150000, type="expense",
        category="Subscription", day_of_month=12, user_id=user.id
    )
    db_session.add(item)
    db_session.commit()

    first = RecurringTransactionService.generate_due_for_user(
        db_session, user.id, as_of=datetime.date(2026, 8, 15)
    )
    assert len(first) == 1
    assert first[0].amount == 150000

    second = RecurringTransactionService.generate_due_for_user(
        db_session, user.id, as_of=datetime.date(2026, 8, 28)
    )
    assert second == []


def test_generates_again_next_month(db_session):

    user = _make_user(db_session)
    item = RecurringTransaction(
        description="Netflix", amount=150000, type="expense",
        category="Subscription", day_of_month=12, user_id=user.id
    )
    db_session.add(item)
    db_session.commit()

    RecurringTransactionService.generate_due_for_user(db_session, user.id, as_of=datetime.date(2026, 8, 15))
    next_month = RecurringTransactionService.generate_due_for_user(db_session, user.id, as_of=datetime.date(2026, 9, 15))

    assert len(next_month) == 1


def test_inactive_recurring_never_generates(db_session):

    user = _make_user(db_session)
    item = RecurringTransaction(
        description="Netflix", amount=150000, type="expense",
        category="Subscription", day_of_month=12, is_active=False, user_id=user.id
    )
    db_session.add(item)
    db_session.commit()

    generated = RecurringTransactionService.generate_due_for_user(
        db_session, user.id, as_of=datetime.date(2026, 8, 20)
    )
    assert generated == []


def test_day_of_month_clamped_to_last_day_of_short_month(db_session):

    user = _make_user(db_session)

    # day_of_month is capped at 28 at the schema layer, so every month
    # has that day — this just verifies the run date is computed correctly.
    item = RecurringTransaction(
        description="Rent", amount=2000000, type="expense",
        category="Bills", day_of_month=28, user_id=user.id
    )
    db_session.add(item)
    db_session.commit()

    generated = RecurringTransactionService.generate_due_for_user(
        db_session, user.id, as_of=datetime.date(2026, 2, 28)
    )
    assert len(generated) == 1
    assert generated[0].date == datetime.date(2026, 2, 28)
