from datetime import timedelta

from fastapi import Depends, HTTPException, status, APIRouter
from sqlalchemy.orm import Session

from leaf.auth import (
    ACCESS_TOKEN_EXPIRE_MINUTES,
    authenticate_user,
    create_access_token,
)
from leaf.database import get_db
from leaf.schemas.users import (
    LoginSchema,
    TokenSchema,
)


router = APIRouter(prefix="/users", tags=["users"])


@router.post("/token", response_model=TokenSchema)
async def login_for_access_token(form_data: LoginSchema, db: Session = Depends(get_db)):
    user = authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.email}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}
