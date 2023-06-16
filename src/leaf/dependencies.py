from os import environ
from typing import Annotated
from functools import lru_cache

from fastapi import Header, HTTPException, status, Depends
from jose import JWTError
from sqlalchemy.orm import Session
from starlette import status

from leaf.auth import oauth2_scheme, verify_token
from leaf.database import get_db
from leaf.models import User
from leaf.repositories.users import get_user_by_email
from leaf.schemas.users import TokenDataSchema
from . import config


@lru_cache()
def get_settings():
    return config.Settings()


async def get_image_size(image_size: Annotated[str, Header(...)],
                         settings: Annotated[config.Settings, Depends(get_settings)]):
    if image_size in settings.AVAILABLE_IMAGE_SIZES:
        return settings.IMAGE_SIZES[image_size][1]

    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                        detail=f"Wrong image size! Available sizes are: {settings.AVAILABLE_IMAGE_SIZES}")


async def get_current_user(
        token: Annotated[str, Depends(oauth2_scheme)], db: Annotated[Session, Depends(get_db)],
        settings: Annotated[config.Settings, Depends(get_settings)]
) -> User:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        username = verify_token(token, secret_key=settings.SECRET_KEY, algorithm=settings.ALGORITHM)
        if username is None:
            raise credentials_exception
        token_data = TokenDataSchema(username=username)
    except JWTError:
        raise credentials_exception
    user = get_user_by_email(db, token_data.username)
    if user is None:
        raise credentials_exception
    return user


async def get_current_active_user(
        current_user: Annotated[User, Depends(get_current_user)]
) -> User:
    if current_user.disabled:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user
