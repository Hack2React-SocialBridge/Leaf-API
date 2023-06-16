from datetime import timedelta, datetime
from os import environ

from fastapi.security import OAuth2PasswordBearer
from jose import jwt
from passlib.context import CryptContext
from sqlalchemy.orm import Session
from itsdangerous import URLSafeTimedSerializer

from leaf.repositories.users import get_user_by_email

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password):
    return pwd_context.hash(password)


def authenticate_user(db: Session, username: str, password: str):
    user = get_user_by_email(db, username)
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user


def create_access_token(data: dict, secret_key: str, algorithm: str, expires_delta: timedelta | None = None):
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


def generate_confirmation_token(email, secret_key: str, security_password_salt: str):
    serializer = URLSafeTimedSerializer(secret_key)
    return serializer.dumps(email, salt=security_password_salt)


Email = str


def confirm_token(token, secret_key: str, security_password_salt: str, expiration=3600) -> Email:
    serializer = URLSafeTimedSerializer(secret_key)
    email = serializer.loads(
        token,
        salt=security_password_salt,
        max_age=expiration
    )
    return email
