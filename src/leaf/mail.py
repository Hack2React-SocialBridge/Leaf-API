import smtplib
from email.mime.multipart import MIMEMultipart
from os import environ


SMTP_EMAIL = environ.get("SMTP_EMAIL")
SMTP_USERNAME = environ.get("SMTP_USERNAME")
SMTP_PASSWORD = environ.get("SMTP_PASSWORD")
SMTP_HOST = environ.get("SMTP_HOST")
SMTP_PORT = environ.get("SMTP_PORT")


def send_mail(to: str, msg: MIMEMultipart):
    with smtplib.SMTP(SMTP_HOST, SMTP_PORT) as server:
        server.starttls()
        server.login(SMTP_USERNAME, SMTP_PASSWORD)
        server.sendmail(
            SMTP_EMAIL, to, msg.as_string()
        )
