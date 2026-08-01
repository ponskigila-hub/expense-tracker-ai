from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import Text
from sqlalchemy import DateTime
from sqlalchemy import Date
from sqlalchemy import Float
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship

from datetime import datetime

from app.database.database import Base


class Receipt(Base):

    __tablename__ = "receipts"

    id = Column(Integer, primary_key=True, index=True)

    user_id = Column(
        Integer,
        ForeignKey("users.id"),
        nullable=False,
        index=True
    )

    # Nullable: a scan can be previewed (auto_save=false) without ever
    # being turned into a transaction.
    transaction_id = Column(
        Integer,
        ForeignKey("transactions.id"),
        nullable=True
    )

    image_path = Column(String, nullable=False)

    raw_text = Column(Text, nullable=False)

    parsed_merchant = Column(String, nullable=True)

    parsed_amount = Column(Float, nullable=True)

    parsed_date = Column(Date, nullable=True)

    created_at = Column(
        DateTime,
        default=datetime.utcnow
    )

    owner = relationship("User")

    transaction = relationship("Transaction")
