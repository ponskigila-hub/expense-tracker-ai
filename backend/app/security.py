from passlib.context import CryptContext
from datetime import datetime
from datetime import timedelta
from datetime import timezone

from jose import jwt

from app.config import settings

from jose import JWTError
from fastapi import Depends
from fastapi import HTTPException
from fastapi import status
from fastapi.security import HTTPBearer
from fastapi.security import HTTPAuthorizationCredentials

from sqlalchemy.orm import Session

from app.database.database import get_db
from app.repositories.user_repository import UserRepository
from app.models.user import User

pwd_context = CryptContext(
    schemes=["bcrypt"],
    deprecated="auto"
)

# HTTPBearer powers the "Authorize" button in Swagger UI.
# Since /login accepts JSON (not the OAuth2 form-encoded spec),
# HTTPBearer is used instead of OAuth2PasswordBearer: paste the
# raw access_token from /login into the Swagger padlock dialog.
bearer_scheme = HTTPBearer(
    bearerFormat="JWT",
    description="Paste the access_token returned by /login"
)



def hash_password(password: str):

    return pwd_context.hash(password)

def verify_password(
    plain_password,
    hashed_password
):

    return pwd_context.verify(
        plain_password,
        hashed_password
    )
    
def create_access_token(
    data: dict
):

    to_encode = data.copy()

    expire = (
        datetime.now(timezone.utc)
        + timedelta(
            minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
        )
    )

    to_encode.update(
        {
            "exp": expire
        }
    )

    return jwt.encode(
        to_encode,
        settings.SECRET_KEY,
        algorithm=settings.ALGORITHM
    )


def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme),
    db: Session = Depends(get_db)
) -> User:

    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"}
    )

    token = credentials.credentials

    try:

        payload = jwt.decode(
            token,
            settings.SECRET_KEY,
            algorithms=[settings.ALGORITHM]
        )

        email: str | None = payload.get("sub")

        if email is None:
            raise credentials_exception

    except JWTError:

        raise credentials_exception

    user = UserRepository.get_by_email(
        db,
        email
    )

    if user is None:
        raise credentials_exception

    return user
