from sqlalchemy import func
from sqlalchemy.orm import Session


def month_expr(db: Session, column):
    """
    Returns a SQLAlchemy expression that formats `column` (a Date/DateTime
    column) as a 'YYYY-MM' string, compiled for whichever database dialect
    the current session is actually connected to.

    strftime() only exists in SQLite — it fails on PostgreSQL with
    "function strftime(unknown, date) does not exist". to_char() is the
    Postgres equivalent. Routing through this helper means the app works
    unmodified whether DATABASE_URL points at SQLite (local/dev default)
    or PostgreSQL (production).
    """

    dialect = db.bind.dialect.name

    if dialect == "postgresql":
        return func.to_char(column, "YYYY-MM")

    # SQLite (and anything else that understands strftime, e.g. during tests)
    return func.strftime("%Y-%m", column)
