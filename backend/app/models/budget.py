from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import Float
from sqlalchemy import ForeignKey
from sqlalchemy import DateTime
from sqlalchemy import UniqueConstraint
from sqlalchemy.orm import relationship

from datetime import datetime

from app.database.database import Base


class Budget(Base):

    __tablename__ = "budgets"

    __table_args__ = (
        UniqueConstraint(
            "user_id",
            "category",
            name="uq_budgets_user_category"
        ),
    )

    id = Column(Integer, primary_key=True, index=True)

    category = Column(String, nullable=False)

    amount = Column(Float, nullable=False)

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

    updated_at = Column(
        DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow
    )

    # "2026-08" — the last calendar month a threshold alert was sent for
    # this budget. Prevents re-notifying every time the checker job runs.
    last_alert_month = Column(String, nullable=True)

    owner = relationship("User", back_populates="budgets")
