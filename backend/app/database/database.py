from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker
from app.config import settings

# Some providers (Heroku-style) still hand back the legacy "postgres://"
# scheme, but SQLAlchemy 2.x + psycopg2 require "postgresql://". Neon
# already gives the correct scheme, but normalizing here costs nothing
# and protects against whichever provider you end up on.
_database_url = settings.DATABASE_URL

if _database_url.startswith("postgres://"):
    _database_url = _database_url.replace("postgres://", "postgresql://", 1)

# check_same_thread is a SQLite-only connect arg — passing it to
# psycopg2 raises a TypeError, so it's only included when actually
# running on SQLite (local dev / Docker default).
_connect_args = (
    {"check_same_thread": False}
    if _database_url.startswith("sqlite")
    else {}
)

engine = create_engine(
    _database_url,
    connect_args=_connect_args
)

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

Base = declarative_base()

def get_db():

    db = SessionLocal()

    try:

        yield db

    finally:

        db.close()