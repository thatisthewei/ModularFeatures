import os
import ssl
import smtplib  # for email sending

from email.message import EmailMessage  # EmailMessage object for easy creating of an email
from dotenv import load_dotenv  # package to easy load .env files

def send_email(recipient: str, subject: str, body: str) -> None:

    """
    Send a plain-text email using the configured SMTP server.
    :param recipient:   recipient's email address
    :param subject:     subject of the email
    :param body:        content of the email
    :return:
    """

    load_dotenv()

    # Set SMTP parameters
    smtp_host = os.environ["SMTP_HOST"]
    smtp_port = int(os.environ["SMTP_PORT"])
    smtp_user = os.environ["SMTP_USER"]
    smtp_password = os.environ["SMTP_PASSWORD"]

    # Create the message
    e_message = EmailMessage()
    e_message["From"] = smtp_user
    e_message["To"] = recipient
    e_message["Subject"] = subject
    e_message.set_content(body)

    # set the context for the email, in this case ssl
    # -> user and log in information necessary
    context = ssl.create_default_context()

    # send email via 'with', automatically ends sending request
    with smtplib.SMTP_SSL(
        smtp_host, smtp_port, context=context, timeout=10
    ) as smtp:
        # login with .env credentials
        smtp.login(smtp_user, smtp_password)
        # send message
        smtp.send_message(e_message)