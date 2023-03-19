import smtplib
from email.message import EmailMessage

from celery import Celery

from src.config import SMTP_USER, SMTP_PASSWORD, SMTP_HOST, SMTP_PORT

celery = Celery('tasks', broker='redis://redis:6379/0',)


def get_email_template(user_email: str, subject: str, text: str, subtype: str):
    email = EmailMessage()
    email['Subject'] = subject
    email['From'] = SMTP_USER
    email['To'] = user_email

    email.set_content(text, subtype=subtype)
    return email


@celery.task
def send_email_report(user_email: str, subject: str, text: str, subtype: str):
    email = get_email_template(user_email, subject, text, subtype)
    with smtplib.SMTP_SSL(SMTP_HOST, SMTP_PORT) as server:
        server.login(SMTP_USER, SMTP_PASSWORD)
        server.send_message(email)
