from datetime import timedelta
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from os import environ

from fastapi import Depends, HTTPException, status, APIRouter, Body, Response
from sqlalchemy.orm import Session
from itsdangerous import BadSignature, SignatureExpired

from leaf.auth import (
    ACCESS_TOKEN_EXPIRE_MINUTES,
    authenticate_user,
    create_access_token,
    get_password_hash,
    confirm_token,
)
from leaf.database import get_db
from leaf.schemas.users import (
    LoginSchema,
    TokenSchema,
    UserSchema,
    UserCreateSchema,
    EmailConfirmationSchema,
    RequestPasswordResetSchema
)
from leaf.schemas.common import DetailsResponseSchema
from leaf.repositories.users import create_one, update_one, get_user_by_email, get_active_user_by_email
from leaf.mail import send_mail
from leaf.jinja_config import env
from leaf.auth import generate_confirmation_token

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


@router.post("/register", response_model=UserSchema, status_code=201)
async def register(user: UserCreateSchema = Body(...), db: Session = Depends(get_db)):
    hashed_password = get_password_hash(user.password)
    db_user = create_one(
        db,
        email=user.email,
        hashed_password=hashed_password,
        first_name=user.first_name,
        last_name=user.last_name,
        disabled=True,
    )

    confirmation_token = generate_confirmation_token(user.email)
    url_template = env.from_string(environ.get("CONFIRMATION_URL"))
    confirm_url = url_template.render(confirmation_token=confirmation_token)

    template = env.get_template("confirmation_email.html")
    msg_content = template.render(confirm_url=confirm_url)
    message = MIMEMultipart("alternative")
    message["Subject"] = "Leaf account - email confirmation"
    message["From"] = environ.get("SMTP_EMAIL")
    message["To"] = user.email
    message.attach(MIMEText(msg_content, "html"))
    send_mail.delay(user.email, message.as_string())

    return db_user


@router.post("/confirm", status_code=200)
async def confirm_user(token: EmailConfirmationSchema = Body(...),
                       db: Session = Depends(get_db)) -> UserSchema | DetailsResponseSchema:
    try:
        email = confirm_token(token.key)
        return update_one(db, user_email=email, disabled=False)
    except (BadSignature, SignatureExpired):
        return Response(DetailsResponseSchema(detail="Invalid token"), status_code=400)


@router.post("/password-reset", status_code=200)
async def password_reset(user: RequestPasswordResetSchema = Body(...),
                         db: Session = Depends(get_db)) -> DetailsResponseSchema:
    db_user = get_active_user_by_email(db, user.email)
    if db_user:
        confirmation_token = generate_confirmation_token(user.email)
        url_template = env.from_string(environ.get("PASSWORD_RESET_URL"))
        reset_url = url_template.render(confirmation_token=confirmation_token)

        template = env.get_template("password_reset.html")
        msg_content = template.render(reset_url=reset_url)
        message = MIMEMultipart("alternative")
        message["Subject"] = "Leaf account - password reset"
        message["From"] = environ.get("SMTP_EMAIL")
        message["To"] = user.email
        message.attach(MIMEText(msg_content, "html"))
        send_mail.delay(user.email, message.as_string())
    return DetailsResponseSchema(detail="Password reset instructions have been sent to the provided email address.")
