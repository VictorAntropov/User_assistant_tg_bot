import smtplib
import ssl
from email.message import EmailMessage

from constants.information import (PROJECT_DIR, PROJECT_EMAIL_QR,
                                   PROJECT_EMAIL_TEXT, PROJECT_FILE_NOT_FOUND,
                                   QR)
from core.settings import settings


def send_message_qr_kod_and_email(user_info):
    try:
        file_dir = f'{PROJECT_DIR}{user_info["number"]}_{QR}.png'
        file_open = open(file_dir, 'rb')
        send_email(user_info, file_dir)
        return file_open
    except FileNotFoundError as e:
        return f'{PROJECT_FILE_NOT_FOUND}: {e}'


def send_email(user_info, file_dir):
    context = ssl.create_default_context()
    sender = settings.sender
    password = settings.password_email
    smtp_server = settings.smtp_server
    port = settings.port
    subject = PROJECT_EMAIL_QR
    body_text = PROJECT_EMAIL_TEXT

    new_message = EmailMessage()
    new_message['Subject'] = subject
    new_message['From'] = sender
    new_message['To'] = user_info["email"]
    new_message.set_content(body_text)

    with open(file_dir, 'rb') as fp:
        img = fp.read()
        new_message.add_attachment(img, maintype='image',
                                   subtype='png', filename='QR-Код.png',)

    with smtplib.SMTP_SSL(
        smtp_server, port, context=context
    ) as server:
        server.login(sender, password)
        server.sendmail(
            sender,
            user_info['email'],
            new_message.as_string())
