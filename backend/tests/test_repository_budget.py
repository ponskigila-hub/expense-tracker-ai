from app.models.user import User
from app.models.budget import Budget
from app.repositories.budget_repository import BudgetRepository
from app.security import pwd_context


def _make_user(db_session, email="budget_repo@test.com") -> User:

    user = User(
        username=email.split("@")[0],
        email=email,
        hashed_password=pwd_context.hash("password123")
    )
    db_session.add(user)
    db_session.commit()
    db_session.refresh(user)

    return user


def test_create_and_get_by_category(db_session):

    user = _make_user(db_session)

    budget = Budget(category="Food", amount=100000, user_id=user.id)
    BudgetRepository.create(db_session, budget)

    found = BudgetRepository.get_by_category(db_session, "Food", user.id)
    assert found is not None
    assert found.amount == 100000

    assert BudgetRepository.get_by_category(db_session, "Transportation", user.id) is None


def test_get_by_id_scoped_to_owner(db_session):

    owner = _make_user(db_session, "owner2@test.com")
    other = _make_user(db_session, "other2@test.com")

    budget = BudgetRepository.create(db_session, Budget(category="Food", amount=100000, user_id=owner.id))

    assert BudgetRepository.get_by_id(db_session, budget.id, other.id) is None
    assert BudgetRepository.get_by_id(db_session, budget.id, owner.id) is not None


def test_get_all_global_spans_users(db_session):

    u1 = _make_user(db_session, "u1@test.com")
    u2 = _make_user(db_session, "u2@test.com")

    BudgetRepository.create(db_session, Budget(category="Food", amount=1, user_id=u1.id))
    BudgetRepository.create(db_session, Budget(category="Food", amount=1, user_id=u2.id))

    assert len(BudgetRepository.get_all_global(db_session)) == 2
    assert len(BudgetRepository.get_all(db_session, u1.id)) == 1
