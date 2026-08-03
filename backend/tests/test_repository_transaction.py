import datetime

from app.models.user import User
from app.models.transaction import Transaction
from app.repositories.transaction_repository import TransactionRepository
from app.security import pwd_context


def _make_user(db_session, email="repo_user@test.com") -> User:

    user = User(
        username=email.split("@")[0],
        email=email,
        hashed_password=pwd_context.hash("password123")
    )
    db_session.add(user)
    db_session.commit()
    db_session.refresh(user)

    return user


def test_create_and_get_by_id(db_session):

    user = _make_user(db_session)

    txn = Transaction(
        date=datetime.date.today(), description="Coffee", amount=30000,
        type="expense", category="Food", user_id=user.id
    )

    created = TransactionRepository.create(db_session, txn)

    assert created.id is not None

    fetched = TransactionRepository.get_by_id(db_session, created.id, user.id)
    assert fetched is not None
    assert fetched.description == "Coffee"


def test_get_by_id_scoped_to_owner(db_session):

    owner = _make_user(db_session, "owner@test.com")
    other = _make_user(db_session, "other@test.com")

    txn = Transaction(
        date=datetime.date.today(), description="Private", amount=1000,
        type="expense", category="Food", user_id=owner.id
    )
    created = TransactionRepository.create(db_session, txn)

    # The other user must never be able to fetch it via this repository call.
    assert TransactionRepository.get_by_id(db_session, created.id, other.id) is None
    assert TransactionRepository.get_by_id(db_session, created.id, owner.id) is not None


def test_delete(db_session):

    user = _make_user(db_session)
    txn = TransactionRepository.create(db_session, Transaction(
        date=datetime.date.today(), description="Temp", amount=1000,
        type="expense", category="Food", user_id=user.id
    ))

    TransactionRepository.delete(db_session, txn)

    assert TransactionRepository.get_by_id(db_session, txn.id, user.id) is None


def test_search_filters_by_category_and_type(db_session):

    user = _make_user(db_session)
    today = datetime.date.today()

    TransactionRepository.create(db_session, Transaction(
        date=today, description="Lunch", amount=50000, type="expense", category="Food", user_id=user.id
    ))
    TransactionRepository.create(db_session, Transaction(
        date=today, description="Salary", amount=5000000, type="income", category="Salary", user_id=user.id
    ))

    items, total = TransactionRepository.search(db_session, user.id, category="Food")
    assert total == 1
    assert items[0].description == "Lunch"

    items, total = TransactionRepository.search(db_session, user.id, type_="income")
    assert total == 1
    assert items[0].description == "Salary"


def test_search_text_is_case_insensitive(db_session):

    user = _make_user(db_session)

    TransactionRepository.create(db_session, Transaction(
        date=datetime.date.today(), description="McDonald's Lunch", amount=1000,
        type="expense", category="Food", user_id=user.id
    ))

    items, total = TransactionRepository.search(db_session, user.id, search="mcdonald")
    assert total == 1


def test_search_amount_range(db_session):

    user = _make_user(db_session)
    today = datetime.date.today()

    for amount in [10000, 50000, 100000]:
        TransactionRepository.create(db_session, Transaction(
            date=today, description=f"Item {amount}", amount=amount,
            type="expense", category="Food", user_id=user.id
        ))

    items, total = TransactionRepository.search(db_session, user.id, min_amount=20000, max_amount=60000)
    assert total == 1
    assert items[0].amount == 50000


def test_search_pagination(db_session):

    user = _make_user(db_session)
    today = datetime.date.today()

    for i in range(5):
        TransactionRepository.create(db_session, Transaction(
            date=today, description=f"Item {i}", amount=1000 + i,
            type="expense", category="Food", user_id=user.id
        ))

    items_p1, total = TransactionRepository.search(db_session, user.id, page=1, page_size=2, sort_by="amount", sort_order="asc")
    items_p2, _ = TransactionRepository.search(db_session, user.id, page=2, page_size=2, sort_by="amount", sort_order="asc")

    assert total == 5
    assert len(items_p1) == 2
    assert len(items_p2) == 2
    assert [t.amount for t in items_p1] == [1000, 1001]
    assert [t.amount for t in items_p2] == [1002, 1003]
