from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import Float
from sqlalchemy import Date
from sqlalchemy import DateTime

from datetime import datetime

from app.database.database import Base


class Transaction(Base):

    __tablename__ = "transactions"

    id = Column(Integer, primary_key=True, index=True)

    date = Column(Date, nullable=False)

    description = Column(String, nullable=False)

    amount = Column(Float, nullable=False)

    type = Column(String, nullable=False)

    category = Column(String, nullable=False)

    notes = Column(String)

    created_at = Column(
        DateTime,
        default=datetime.utcnow
    )