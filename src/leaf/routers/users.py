from pathlib import Path
from datetime import timedelta
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from os import environ

from fastapi import Depends, HTTPException, status, APIRouter, Body, UploadFile
from fastapi.exceptions import HTTPException
from fastapi.responses import JSONResponse
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
from leaf.dependencies import get_image_size, get_current_active_user
from leaf.schemas.users import (
    LoginSchema,
    TokenSchema,
    UserSchema,
    UserCreateSchema,
    EmailConfirmationSchema,
    RequestPasswordResetSchema,
    PasswordResetSchema,
)
from leaf.repositories.users import create_one, update_one, get_user_by_email, get_active_user_by_email
from leaf.tasks import resize_image, send_mail
from leaf.jinja_config import env
from leaf.media import flush_old_media_resources, create_media_resource, get_media_image_url, get_resource_absolute_path
from leaf.auth import generate_confirmation_token
from leaf.models import User

router = APIRouter(prefix="/users", tags=["users"])

MEDIA_FOLDER = environ.get("MEDIA_FOLDER")
MEDIA_BASE_URL = environ.get("MEDIA_BASE_URL")
AVAILABLE_IMAGE_SIZES = environ.get("AVAILABLE_IMAGE_SIZES")
IMAGE_SIZES = {size: environ.get(f"{size.upper()}_IMAGE_SIZE").split("x") for size in AVAILABLE_IMAGE_SIZES.split(",")}


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
                       db: Session = Depends(get_db)) -> UserSchema:
    try:
        email = confirm_token(token.key)
        return update_one(db, user_email=email, disabled=False)
    except (BadSignature, SignatureExpired):
        raise HTTPException(status_code=400, detail="Invalid token")


@router.post("/password-reset", status_code=200)
async def password_reset(user: RequestPasswordResetSchema = Body(...),
                         db: Session = Depends(get_db)):
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
    return JSONResponse(
        {"detail": "Password reset instructions have been sent to the provided email address."}, status_code=200)


@router.post("/password-reset-confirm", status_code=200)
async def password_reset_confirm(body: PasswordResetSchema = Body(...), db: Session = Depends(get_db)) -> UserSchema:
    try:
        email = confirm_token(body.key)
        new_password_hash = get_password_hash(body.new_password)
        return update_one(db, user_email=email, hashed_password=new_password_hash)
    except (BadSignature, SignatureExpired):
        raise HTTPException(status_code=400, detail="Invalid token")


@router.put("/user-image")
async def update_user_image(image: UploadFile, current_user: User = Depends(get_current_active_user),
                            image_size: str = Depends(get_image_size), db: Session = Depends(get_db)):
    image_format = image.filename.split(".")[-1]
    relative_image_path = Path(f"{current_user.id}/user_image.{image_format}")
    absolute_image_path = get_resource_absolute_path(relative_image_path)

    flush_old_media_resources(absolute_image_path)
    create_media_resource(absolute_image_path, await image.read())
    resize_image.delay(str(absolute_image_path))

    db_user = update_one(db, current_user.email, profile_image=str(relative_image_path.name))
    user_data = db_user.__dict__
    del user_data["profile_image"]
    return UserSchema(**db_user.__dict__, profile_image=get_media_image_url(relative_image_path, image_size))
