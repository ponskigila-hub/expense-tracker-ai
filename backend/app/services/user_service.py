from sqlalchemy.orm import Session

from fastapi import HTTPException

from app.models.user import User

from app.schemas.user import UserCreate

from app.repositories.user_repository import UserRepository

from app.security import hash_password


class UserService:

    @staticmethod
    def register_user(
        db: Session,
        user_data: UserCreate
    ):

        # Check if email already exists
        existing_email = UserRepository.get_by_email(
            db,
            user_data.email
        )

        if existing_email:
            raise HTTPException(
                status_code=409,
                detail="Email already registered"
            )

        # Check if username already exists
        existing_username = UserRepository.get_by_username(
            db,
            user_data.username
        )

        if existing_username:
            raise HTTPException(
                status_code=409,
                detail="Username already exists"
            )

        # Hash password
        hashed_password = hash_password(
            user_data.password
        )

        # Create user object
        user = User(
            username=user_data.username,
            email=user_data.email,
            hashed_password=hashed_password
        )

        # Save user
        return UserRepository.create(
            db,
            user
        )