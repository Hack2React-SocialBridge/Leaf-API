from __future__ import annotations

from functools import lru_cache

from environs import Env
from pydantic import BaseSettings

env = Env()


class Settings(BaseSettings):
    DB_CONFIG = {
        "USER": env("POSTGRES_USER"),
        "PASSWORD": env("POSTGRES_PASSWORD"),
        "HOST": env("POSTGRES_HOST"),
        "PORT": env("POSTGRES_PORT"),
        "DATABASE": env("POSTGRES_DB"),
    }

    LOG_LEVEL = env.log_level("LOG_LEVEL")

    SECRET_KEY = env("SECRET_KEY")
    SECURITY_PASSWORD_SALT = env("SECURITY_PASSWORD_SALT")
    ALGORITHM = env("ALGORITHM")
    ACCESS_TOKEN_EXPIRE_MINUTES = env.int("ACCESS_TOKEN_EXPIRE_MINUTES")

    CELERY_BROKER_URL = env("CELERY_BROKER_URL")
    CELERY_RESULT_BACKEND = env("CELERY_RESULT_BACKEND")

    AVAILABLE_IMAGE_SIZES = env("AVAILABLE_IMAGE_SIZES")
    IMAGE_SIZES = {
        size: env(f"{size.upper()}_IMAGE_SIZE").split("x")
        for size in AVAILABLE_IMAGE_SIZES.split(",")
    }

    MEDIA_FOLDER = env("MEDIA_FOLDER")
    MEDIA_BASE_URL = env("MEDIA_BASE_URL")

    CONFIRMATION_URL = env("CONFIRMATION_URL")
    PASSWORD_RESET_URL = env("PASSWORD_RESET_URL")

    SMTP_CONFIG = {
        "EMAIL": env("SMTP_EMAIL"),
        "USERNAME": env("SMTP_USERNAME"),
        "PASSWORD": env("SMTP_PASSWORD"),
        "HOST": env("SMTP_HOST"),
        "PORT": env("SMTP_PORT"),
    }


@lru_cache
def get_settings():
    return Settings()
