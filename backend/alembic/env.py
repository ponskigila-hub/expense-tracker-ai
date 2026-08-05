from logging.config import fileConfig

from alembic import context
from app.database.database import Base, engine
from app.models.transaction import Transaction
from app.models.user import User
from app.models.budget import Budget
from app.models.receipt import Receipt
from app.models.recurring_transaction import RecurringTransaction

# this is the Alembic Config object, which provides
# access to the values within the .ini file in use.
config = context.config

# Interpret the config file for Python logging.
# This line sets up loggers basically.
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# add your model's MetaData object here
# for 'autogenerate' support
# from myapp import mymodel
# target_metadata = mymodel.Base.metadata

target_metadata = Base.metadata

# Deliberately NOT using alembic.ini's `sqlalchemy.url` (or
# engine_from_config) here. The app's real engine — built from
# DATABASE_URL in .env, see app/database/database.py — is reused
# directly instead, so migrations always target whatever database the
# app itself is actually configured for (SQLite locally, Postgres in
# production) with zero duplicated config to keep in sync.


def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode.

    This configures the context with just a URL
    and not an Engine, though an Engine is acceptable
    here as well.  By skipping the Engine creation
    we don't even need a DBAPI to be available.

    Calls to context.execute() here emit the given string to the
    script output.

    """
    url = engine.url.render_as_string(hide_password=False)
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    """Run migrations in 'online' mode.

    In this scenario we need to create an Engine
    and associate a connection with the context.

    """
    with engine.connect() as connection:
        context.configure(
            connection=connection, target_metadata=target_metadata
        )

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
