from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import Float
from sqlalchemy import Boolean
from sqlalchemy import Date
from sqlalchemy import DateTime
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship

from datetime import datetime

from app.database.database import Base


class RecurringTransaction(Base):

    __tablename__ = "recurring_transactions"

    id = Column(Integer, primary_key=True, index=True)

    description = Column(String, nullable=False)

    amount = Column(Float, nullable=False)

    type = Column(String, nullable=False)

    category = Column(String, nullable=False)

    notes = Column(String, nullable=True)

    # Day of month this recurs on. Capped at 28 at the API layer so it
    # always exists in every month (no Feb 30th surprises).
    day_of_month = Column(Integer, nullable=False)

    is_active = Column(Boolean, default=True, nullable=False)

    # Last calendar month this template successfully generated a
    # transaction for — prevents double-generation if the scheduler
    # runs more than once in the same month.
    last_run_date = Column(Date, nullable=True)

    user_id = Column(
        Integer,
        ForeignKey("users.id"),
        nullable=False,
        index=True
    )

    created_at = Column(
        DateTime,
        default=datetime.utcnow
    )

    owner = relationship("User", back_populates="recurring_transactions")
