from sqlalchemy.orm import Session

from app.models.transaction import Transaction


class TransactionRepository:

    @staticmethod
    def create(
        db: Session,
        transaction: Transaction
    ):

        db.add(transaction)

        db.commit()

        db.refresh(transaction)

        return transaction
    
    @staticmethod
    def get_all(
        db: Session,
        user_id: int
    ):

        return (
            db.query(Transaction)
            .filter(Transaction.user_id == user_id)
            .all()
        )
    
    @staticmethod
    def get_by_id(
        db: Session,
        transaction_id: int,
        user_id: int
    ):

        return (
            db.query(Transaction)
            .filter(
                Transaction.id == transaction_id,
                Transaction.user_id == user_id
            )
            .first()
        )
        
    @staticmethod
    def update(
        db: Session,
        transaction: Transaction
    ):

        db.commit()

        db.refresh(transaction)

        return transaction
    
    @staticmethod
    def delete(
        db: Session,
        transaction: Transaction
    ):

        db.delete(transaction)

        db.commit()