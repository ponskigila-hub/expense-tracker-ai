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
    def search(
        db: Session,
        user_id: int,
        category: str | None = None,
        type_: str | None = None,
        date_from=None,
        date_to=None,
        min_amount: float | None = None,
        max_amount: float | None = None,
        search: str | None = None,
        sort_by: str = "date",
        sort_order: str = "desc",
        page: int = 1,
        page_size: int = 20,
    ):

        query = db.query(Transaction).filter(Transaction.user_id == user_id)

        if category:
            query = query.filter(Transaction.category == category)

        if type_:
            query = query.filter(Transaction.type == type_)

        if date_from:
            query = query.filter(Transaction.date >= date_from)

        if date_to:
            query = query.filter(Transaction.date <= date_to)

        if min_amount is not None:
            query = query.filter(Transaction.amount >= min_amount)

        if max_amount is not None:
            query = query.filter(Transaction.amount <= max_amount)

        if search:
            like_pattern = f"%{search}%"
            query = query.filter(Transaction.description.ilike(like_pattern))

        total = query.count()

        sort_columns = {
            "date": Transaction.date,
            "amount": Transaction.amount,
            "description": Transaction.description,
            "category": Transaction.category,
            "created_at": Transaction.created_at,
        }
        sort_column = sort_columns.get(sort_by, Transaction.date)

        if sort_order == "asc":
            query = query.order_by(sort_column.asc())
        else:
            query = query.order_by(sort_column.desc())

        items = (
            query
            .offset((page - 1) * page_size)
            .limit(page_size)
            .all()
        )

        return items, total

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