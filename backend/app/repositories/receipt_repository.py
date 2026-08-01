from sqlalchemy.orm import Session

from app.models.receipt import Receipt


class ReceiptRepository:

    @staticmethod
    def create(
        db: Session,
        receipt: Receipt
    ):

        db.add(receipt)

        db.commit()

        db.refresh(receipt)

        return receipt

    @staticmethod
    def get_all(
        db: Session,
        user_id: int
    ):

        return (
            db.query(Receipt)
            .filter(Receipt.user_id == user_id)
            .order_by(Receipt.created_at.desc())
            .all()
        )

    @staticmethod
    def get_by_id(
        db: Session,
        receipt_id: int,
        user_id: int
    ):

        return (
            db.query(Receipt)
            .filter(
                Receipt.id == receipt_id,
                Receipt.user_id == user_id
            )
            .first()
        )
