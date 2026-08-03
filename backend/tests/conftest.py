import sys
import os
import uuid

import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool
from fastapi.testclient import TestClient

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Import every model so Base.metadata knows about all tables before
# create_all() runs below.
from app.database.database import Base, get_db
from app.models.user import User          # noqa: F401
from app.models.transaction import Transaction  # noqa: F401
from app.models.budget import Budget      # noqa: F401
from app.models.receipt import Receipt    # noqa: F401
from app.models.recurring_transaction import RecurringTransaction  # noqa: F401

from app.main import app


@pytest.fixture()
def db_session():
    """
    Fresh, fully isolated SQLite in-memory database per test. Using
    StaticPool keeps a single connection alive for the whole test so
    the in-memory DB doesn't disappear between statements.
    """

    engine = create_engine(
        "sqlite:///:memory:",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )

    Base.metadata.create_all(bind=engine)

    TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    session = TestingSessionLocal()

    try:
        yield session
    finally:
        session.close()
        Base.metadata.drop_all(bind=engine)


@pytest.fixture()
def client(db_session):
    """TestClient wired to the isolated test DB instead of the real dev
    database, via FastAPI's dependency override mechanism."""

    def override_get_db():
        try:
            yield db_session
        finally:
            pass

    app.dependency_overrides[get_db] = override_get_db

    with TestClient(app) as test_client:
        yield test_client

    app.dependency_overrides.clear()


@pytest.fixture()
def make_user(client):
    """Factory fixture: make_user() -> (user_email, auth_headers).
    Each call registers a fresh, unique user so tests can easily spin up
    multiple independent accounts (e.g. for cross-user isolation tests)."""

    def _make_user(username: str | None = None):

        unique = uuid.uuid4().hex[:8]
        username = username or f"user_{unique}"
        email = f"{username}@test.com"
        password = "password123"

        r = client.post("/register", json={
            "username": username, "email": email, "password": password
        })
        assert r.status_code == 201, r.text

        l = client.post("/login", json={"email": email, "password": password})
        assert l.status_code == 200, l.text

        token = l.json()["access_token"]
        headers = {"Authorization": f"Bearer {token}"}

        return email, headers

    return _make_user


@pytest.fixture()
def auth_headers(make_user):
    """Convenience fixture for tests that only need one logged-in user."""
    _, headers = make_user()
    return headers
