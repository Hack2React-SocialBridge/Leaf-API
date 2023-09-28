from __future__ import annotations

from datetime import datetime, timedelta
from os import environ
from typing import Annotated

from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from itsdangerous import URLSafeTimedSerializer
from jose import JWTError, jwt
from passlib.context import CryptContext
from sqlalchemy.orm import Session
from starlette import status

from leaf.config import config
from leaf.config.config import get_settings
from leaf.config.database import get_db
from leaf.media import get_image_size
from leaf.models import User
from leaf.repositories.users import get_user_by_email
from leaf.schemas.users import TokenDataSchema

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password):
    return pwd_context.hash(password)


def authenticate_user(db: Session, username: str, password: str):
    user = db.query(User).filter(User.disabled == False, User.email == username).first()
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user


def create_access_token(
    data: dict,
    secret_key: str,
    algorithm: str,
    expires_delta: timedelta | None = None,
):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, secret_key, algorithm=algorithm)
    return encoded_jwt


def verify_token(token: str, secret_key: str, algorithm: str) -> str | None:
    payload = jwt.decode(token, secret_key, algorithms=[algorithm])
    username: str = payload.get("sub")
    return username


def generate_confirmation_token(
    email,
    secret_key: str,
    security_password_salt: str,
):
    serializer = URLSafeTimedSerializer(secret_key)
    return serializer.dumps(email, salt=security_password_salt)


Email = str


def confirm_token(
    token,
    secret_key: str,
    security_password_salt: str,
    expiration=3600,
) -> Email:
    serializer = URLSafeTimedSerializer(secret_key)
    email = serializer.loads(
        token,
        salt=security_password_salt,
        max_age=expiration,
    )
    return email


async def get_current_user(
    token: Annotated[str, Depends(oauth2_scheme)],
    db: Annotated[Session, Depends(get_db)],
    settings: Annotated[config.Settings, Depends(get_settings)],
    image_size: Annotated[int, Depends(get_image_size)],
) -> User:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        username = verify_token(
            token,
            secret_key=settings.SECRET_KEY,
            algorithm=settings.ALGORITHM,
        )
        if username is None:
            raise credentials_exception
        token_data = TokenDataSchema(username=username)
    except JWTError:
        raise credentials_exception
    user = get_user_by_email(db, token_data.username, image_size)
    if user is None:
        raise credentials_exception
    return user


async def get_current_active_user(
    current_user: Annotated[User, Depends(get_current_user)],
) -> User:
    if current_user.disabled:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user
