from sqlalchemy.orm import Session

from fastapi import HTTPException

from app.models.user import User

from app.schemas.user import (
    UserCreate,
    UserLogin,
)

from app.repositories.user_repository import UserRepository

from app.security import (
    hash_password,
    verify_password,
    create_access_token,
)


class UserService:

    @staticmethod
    def register_user(
        db: Session,
        user_data: UserCreate
    ) -> User:

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

    @staticmethod
    def login(
        db: Session,
        credentials: UserLogin
    ) -> dict:

        # Find user by email
        user = UserRepository.authenticate(
            db,
            credentials.email
        )

        if user is None:
            raise HTTPException(
                status_code=401,
                detail="Invalid email or password"
            )

        # Verify password
        if not verify_password(
            credentials.password,
            user.hashed_password
        ):
            raise HTTPException(
                status_code=401,
                detail="Invalid email or password"
            )

        # Generate JWT access token
        access_token = create_access_token(
            {
                "sub": user.email
            }
        )

        return {
            "access_token": access_token,
            "token_type": "bearer"
        }