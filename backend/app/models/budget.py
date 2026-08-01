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

    owner = relationship("User", back_populates="budgets")
