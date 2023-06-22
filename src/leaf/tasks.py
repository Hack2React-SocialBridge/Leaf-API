from __future__ import annotations

import smtplib
from os import remove
from pathlib import Path
from typing import Sequence, Tuple

from celery import shared_task
from PIL import Image

from leaf.logger import logger

Width = str
Height = str
Size = Tuple[Width, Height]


@shared_task
def resize_image(file_path: str, image_sizes: Sequence[Size]):
    path = Path(file_path)
    for width, height in image_sizes:
        size = (
            int(width),
            int(height),
        )
        image = Image.open(path, mode="r")
        image.thumbnail(size)
        image.save(
            str(path.parent) + "/" + str(height) + "_" + str(path.name),
        )
    logger.debug(f"Image resized to all formats")
    remove(path)
    logger.debug(f"Base image removed from path: {file_path}")


@shared_task
def send_mail(to: str, msg: str, smtp_config: dict):
    with smtplib.SMTP(smtp_config["HOST"], smtp_config["PORT"]) as server:
        server.starttls()
        server.login(smtp_config["USERNAME"], smtp_config["PASSWORD"])
        server.sendmail(smtp_config["EMAIL"], to, msg)
    logger.debug("Message sent", extra={"user": to})
