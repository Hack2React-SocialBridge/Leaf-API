import smtplib
from os import environ, remove
from pathlib import Path

from celery import shared_task
from PIL import Image

AVAILABLE_IMAGE_SIZES = environ.get("AVAILABLE_IMAGE_SIZES")
IMAGE_SIZES = {size: environ.get(f"{size.upper()}_IMAGE_SIZE").split("x") for size in AVAILABLE_IMAGE_SIZES.split(",")}
SMTP_EMAIL = environ.get("SMTP_EMAIL")
SMTP_USERNAME = environ.get("SMTP_USERNAME")
SMTP_PASSWORD = environ.get("SMTP_PASSWORD")
SMTP_HOST = environ.get("SMTP_HOST")
SMTP_PORT = environ.get("SMTP_PORT")


@shared_task
def resize_image(file_path: str):
    path = Path(file_path)
    for width, height in IMAGE_SIZES.values():
        size = (int(width), int(height),)
        image = Image.open(path, mode="r")
        image.thumbnail(size)
        image.save(str(path.parent) + "/" + height + "_" + str(path.name))
    remove(path)


@shared_task
def send_mail(to: str, msg: str):
    with smtplib.SMTP(SMTP_HOST, SMTP_PORT) as server:
        server.starttls()
        server.login(SMTP_USERNAME, SMTP_PASSWORD)
        server.sendmail(
            SMTP_EMAIL, to, msg
        )
