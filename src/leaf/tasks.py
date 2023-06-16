import smtplib
from os import remove
from pathlib import Path

from celery import shared_task
from PIL import Image


Width = int
Height = int


@shared_task
def resize_image(file_path: str, image_sizes: list[Width, Height]):
    path = Path(file_path)
    for width, height in image_sizes:
        size = (int(width), int(height),)
        image = Image.open(path, mode="r")
        image.thumbnail(size)
        image.save(str(path.parent) + "/" + height + "_" + str(path.name))
    remove(path)


@shared_task
def send_mail(to: str, msg: str, smtp_config: dict):
    with smtplib.SMTP(smtp_config["HOST"], smtp_config["PORT"]) as server:
        server.starttls()
        server.login(smtp_config["USERNAME"], smtp_config["PASSWORD"])
        server.sendmail(
            smtp_config["EMAIL"], to, msg
        )
