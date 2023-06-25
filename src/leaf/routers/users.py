from __future__ import annotations

from datetime import timedelta
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from pathlib import Path

from fastapi import (
    APIRouter,
    Body,
    Depends,
    HTTPException,
    Request,
    UploadFile,
    status,
)
from fastapi.responses import JSONResponse
from itsdangerous import BadSignature, SignatureExpired
from sqlalchemy.orm import Session

from leaf.auth import (
    authenticate_user,
    confirm_token,
    create_access_token,
    generate_confirmation_token,
    get_current_active_user,
    get_password_hash,
)
from leaf.config.config import Settings, get_settings
from leaf.config.database import get_db
from leaf.config.jinja_config import env
from leaf.config.logger import logger
from leaf.media import (
    create_media_resource,
    flush_old_media_resources,
    get_image_size,
    get_media_image_url,
    get_resource_absolute_path,
)
from leaf.models.user import User
from leaf.repositories.users import (
    create_one,
    get_active_user_by_email,
    update_one,
)
from leaf.schemas.users import (
    EmailConfirmationSchema,
    GroupProfileSchema,
    LoginSchema,
    PasswordResetSchema,
    PermissionsSchema,
    RequestPasswordResetSchema,
    TokenSchema,
    UserCreateSchema,
    UserSchema,
)
from leaf.tasks import resize_image, send_mail

router = APIRouter(prefix="/users", tags=["users"])


@router.post("/token", response_model=TokenSchema)
async def login_for_access_token(
    request: Request,
    form_data: LoginSchema,
    db: Session = Depends(get_db),
    settings: Settings = Depends(get_settings),
):
    user = authenticate_user(db, form_data.username, form_data.password)
    if not user:
        logger.info(
            f"Invalid credentials provided",
            extra={
                "url": "/token",
                "method": "POST",
                "ip": request.client.host,
                "user": user.email,
            },
        )
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    logger.debug(
        "Credentials successful authenticated",
        extra={
            "url": "/token",
            "method": "POST",
            "ip": request.client.host,
            "user": user.email,
        },
    )
    access_token_expires = timedelta(
        minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES,
    )
    access_token = create_access_token(
        data={"sub": user.email},
        secret_key=settings.SECRET_KEY,
        algorithm=settings.ALGORITHM,
        expires_delta=access_token_expires,
    )
    logger.debug(
        "Access token generated",
        extra={
            "url": "/token",
            "method": "POST",
            "ip": request.client.host,
            "user": user.email,
        },
    )
    logger.info(
        "User successful generated token",
        extra={
            "url": "/token",
            "method": "POST",
            "ip": request.client.host,
            "user": user.email,
        },
    )
    db_user = get_active_user_by_email(db, email=user.email)
    return TokenSchema(access_token=access_token, token_type="bearer", user=db_user)


@router.post("/register", response_model=UserSchema, status_code=201)
async def register(
    request: Request,
    user: UserCreateSchema = Body(...),
    db: Session = Depends(get_db),
    settings: Settings = Depends(get_settings),
):
    hashed_password = get_password_hash(user.password)
    db_user = create_one(
        db,
        email=user.email,
        hashed_password=hashed_password,
        first_name=user.first_name,
        last_name=user.last_name,
        disabled=True,
    )
    logger.debug(
        "User created in database",
        extra={
            "url": "/registered",
            "method": "POST",
            "ip": request.client.host,
            "user": user.email,
        },
    )
    confirmation_token = generate_confirmation_token(
        user.email,
        secret_key=settings.SECRET_KEY,
        security_password_salt=settings.SECURITY_PASSWORD_SALT,
    )
    logger.debug(
        "Confirmation token generated",
        extra={
            "url": "/registered",
            "method": "POST",
            "ip": request.client.host,
            "user": user.email,
        },
    )
    url_template = env.from_string(settings.CONFIRMATION_URL)
    confirm_url = url_template.render(
        confirmation_token=confirmation_token,
    )
    template = env.get_template("confirmation_email.html")
    msg_content = template.render(confirm_url=confirm_url)
    message = MIMEMultipart("alternative")
    message["Subject"] = "Leaf account - email confirmation"
    message["From"] = settings.SMTP_CONFIG["EMAIL"]
    message["To"] = user.email
    message.attach(MIMEText(msg_content, "html"))
    send_mail.delay(
        user.email,
        message.as_string(),
        settings.SMTP_CONFIG,
    )
    logger.info(
        f"New user registered",
        extra={
            "url": "/registered",
            "method": "POST",
            "ip": request.client.host,
            "user": db_user.email,
        },
    )
    permissions = db_user.mapped_permissions
    data = db_user.__dict__
    del data["permissions"]
    return UserSchema(**data, permissions=PermissionsSchema(**permissions), groups=[])


@router.post("/confirm", status_code=200)
async def confirm_user(
    request: Request,
    token: EmailConfirmationSchema = Body(...),
    db: Session = Depends(get_db),
    settings: Settings = Depends(get_settings),
    image_size: int = Depends(get_image_size),
) -> UserSchema:
    token_exception = HTTPException(
        status_code=400,
        detail="Invalid token",
    )
    try:
        email = confirm_token(
            token.key,
            secret_key=settings.SECRET_KEY,
            security_password_salt=settings.SECURITY_PASSWORD_SALT,
        )
        logger.info(
            f"User successful finished email confirmation",
            extra={
                "url": "/confirm",
                "method": "POST",
                "ip": request.client.host,
                "user": email,
            },
        )
        update_one(db, user_email=email, disabled=False)
        return get_active_user_by_email(db, email, image_size)
    except BadSignature:
        logger.debug(
            "Invalid token provided",
            extra={
                "url": "/confirm",
                "method": "POST",
                "ip": str(request.client.host),
            },
        )
        raise token_exception

    except SignatureExpired:
        logger.debug(
            "Expired token provided",
            extra={
                "url": "/confirm",
                "method": "POST",
                "ip": request.client.host,
            },
        )
        raise token_exception


@router.post("/password-reset", status_code=200)
async def password_reset(
    request: Request,
    user: RequestPasswordResetSchema = Body(...),
    db: Session = Depends(get_db),
    settings: Settings = Depends(get_settings),
):
    db_user = get_active_user_by_email(db, user.email)
    if db_user:
        confirmation_token = generate_confirmation_token(
            user.email,
            secret_key=settings.SECRET_KEY,
            security_password_salt=settings.SECURITY_PASSWORD_SALT,
        )
        logger.debug(
            "Confirmation token generated",
            extra={
                "url": "/password_reset",
                "method": "POST",
                "ip": request.client.host,
                "user": user.email,
            },
        )
        url_template = env.from_string(settings.PASSWORD_RESET_URL)
        reset_url = url_template.render(
            confirmation_token=confirmation_token,
        )

        template = env.get_template("password_reset.html")
        msg_content = template.render(reset_url=reset_url)
        message = MIMEMultipart("alternative")
        message["Subject"] = "Leaf account - password reset"
        message["From"] = settings.SMTP_CONFIG["EMAIL"]
        message["To"] = user.email
        message.attach(MIMEText(msg_content, "html"))
        send_mail.delay(user.email, message.as_string())

        logger.info(
            "User started password reset process",
            extra={
                "url": "/password_reset",
                "method": "POST",
                "ip": request.client.host,
                "user": user.email,
            },
        )
    else:
        logger.debug(
            "Invalid email provided for password reset",
            extra={
                "url": "/password_reset",
                "method": "POST",
                "ip": request.client.host,
                "user": user.email,
            },
        )
    return JSONResponse(
        {
            "detail": "Password reset instructions have been sent to the provided email address.",
        },
        status_code=200,
    )


@router.post("/password-reset-confirm", status_code=200)
async def password_reset_confirm(
    request: Request,
    body: PasswordResetSchema = Body(...),
    db: Session = Depends(get_db),
    image_size: int = Depends(get_image_size),
    settings: Settings = Depends(get_settings),
) -> UserSchema:
    token_exception = HTTPException(
        status_code=400,
        detail="Invalid token",
    )
    try:
        email = confirm_token(
            body.key,
            secret_key=settings.SECRET_KEY,
            security_password_salt=settings.SECURITY_PASSWORD_SALT,
        )
        logger.debug(
            "Token successful confirmed",
            extra={
                "url": "/password_reset-confirm",
                "method": "POST",
                "ip": request.client.host,
            },
        )
        new_password_hash = get_password_hash(body.new_password)
        update_one(
            db,
            user_email=email,
            hashed_password=new_password_hash,
        )
        logger.debug(
            "User hashed_password changed",
            extra={
                "url": "/password_reset-confirm",
                "method": "POST",
                "ip": request.client.host,
                "user": email,
            },
        )
        logger.info(
            "User finished password change",
            extra={
                "url": "/password_reset-confirm",
                "method": "POST",
                "ip": request.client.host,
            },
        )
        return get_active_user_by_email(db, email, image_size)
    except BadSignature:
        logger.info(
            "User provided invalid token",
            extra={
                "url": "/password_reset-confirm",
                "method": "POST",
                "ip": request.client.host,
            },
        )
        raise token_exception
    except SignatureExpired:
        logger.info(
            "User provided expired token",
            extra={
                "url": "/password_reset-confirm",
                "method": "POST",
                "ip": request.client.host,
            },
        )
        raise token_exception


@router.put("/user-image")
async def update_user_image(
    request: Request,
    image: UploadFile,
    current_user: User = Depends(get_current_active_user),
    image_size: str = Depends(get_image_size),
    db: Session = Depends(get_db),
    settings: Settings = Depends(get_settings),
):
    image_format = image.filename.split(".")[-1]
    relative_image_path = Path(
        f"{current_user.id}/user_image.{image_format}",
    )
    absolute_image_path = get_resource_absolute_path(
        relative_image_path,
        media_folder=settings.MEDIA_FOLDER,
    )

    flush_old_media_resources(absolute_image_path)
    logger.debug(
        "Old media files removed from the volume",
        extra={
            "url": "/user-image",
            "method": "POST",
            "ip": request.client.host,
            "user": current_user.email,
        },
    )

    create_media_resource(absolute_image_path, await image.read())
    logger.dbug(
        "Base image saved on the volume",
        extra={
            "url": "/user-image",
            "method": "POST",
            "ip": request.client.host,
            "user": current_user.email,
        },
    )
    resize_image.delay(
        str(absolute_image_path),
        list(settings.IMAGE_SIZES.values()),
    )

    update_one(
        db,
        current_user.email,
        image_size,
        settings,
        profile_image=str(relative_image_path.name),
    )
    logger.info(
        "User changed image successful",
        extra={
            "url": "/user-image",
            "method": "POST",
            "ip": request.client.host,
            "user": current_user.email,
        },
    )
    return get_active_user_by_email(db, current_user.email, image_size)
