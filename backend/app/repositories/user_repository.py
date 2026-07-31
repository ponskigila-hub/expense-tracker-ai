from sqlalchemy.orm import Session

from app.models.user import User


class UserRepository:

    @staticmethod
    def create(
        db: Session,
        user: User
    ):

        db.add(user)

        db.commit()

        db.refresh(user)

        return user
    
    @staticmethod
    def get_by_email(
        db: Session,
        email: str
    ):

        return (
            db.query(User)
            .filter(User.email == email)
            .first()
        )
        
    @staticmethod
    def get_by_username(
        db: Session,
        username: str
    ):

        return (
            db.query(User)
            .filter(User.username == username)
            .first()
        )
        
    @staticmethod
    def authenticate(
        db: Session,
        email: str
    ):

        return (
            db.query(User)
            .filter(User.email == email)
            .first()
        )