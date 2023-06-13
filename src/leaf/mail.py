import smtplib
from email.mime.multipart import MIMEMultipart
from os import environ

from celery import shared_task


SMTP_EMAIL = environ.get("SMTP_EMAIL")
SMTP_USERNAME = environ.get("SMTP_USERNAME")
SMTP_PASSWORD = environ.get("SMTP_PASSWORD")
SMTP_HOST = environ.get("SMTP_HOST")
SMTP_PORT = environ.get("SMTP_PORT")


@shared_task
def send_mail(to: str, msg: str):
    with smtplib.SMTP(SMTP_HOST, SMTP_PORT) as server:
        server.starttls()
        server.login(SMTP_USERNAME, SMTP_PASSWORD)
        server.sendmail(
            SMTP_EMAIL, to, msg
        )
