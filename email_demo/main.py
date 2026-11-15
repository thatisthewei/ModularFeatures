import os
import smtplib

from dotenv import load_dotenv
from src.email_sender import send_email
from src.recipients import get_recipients_by_topic
from src.template_renderer import render_template


def test_template(template_name: str, send_messages: bool = False):
    topic = "topic_a"

    recipients = get_recipients_by_topic(topic)

    for recipient in recipients:

        if template_name == "topic_notification":
            body = render_template(
                "topic_notification",
                {
                    "name": recipient["name"],
                    "topic": "Topic A",
                    "content": "There has been new updates about Topic A.",
                },
            )
            subject = "New update about Topic A"
        elif template_name == "registration_success":
            body = render_template(
                "registration_success",
                {
                    "name": recipient["name"],
                }
            )
            subject = "Your registration was successful!"
        elif template_name == "deadline_reminder":
            body = render_template(
                "deadline_reminder",
                {
                    "name": recipient["name"],
                    "subject": "Application Deadline",
                    "topic": "Topic A",
                    "time": "7 days"
                }
            )
            subject = "Reminder for incoming deadline."
        elif template_name == "login_code":
            body = render_template(
                "login_code",
                {
                    "name": recipient["name"],
                    "code": "123456"
                }
            )
            subject = "Your login code."
        else:
            raise ValueError(f"Unknown template {template_name}")

        if send_messages:
            send_email(
                recipient=recipient["email"],
                subject=subject,
                body=body,
            )
            print(f"Submitted to SMTP: {recipient['email']}")
        else:
            print(f"To: {recipient['email']}")
            print(f"Subject: {subject}")
            print(body)
            print("-" * 40)

    print(f"Processed {len(recipients)} recipients.")


def test_send_email():
    """
    Only run this method, if you want to actually test the sending of an email.
    I recommend using your own email as sender and receiver.
    Adjust the .env variables accordingly.
    :return:
    """
    load_dotenv()

    recipient = os.environ["SMTP_USER"]

    subject = "Test Email via Python"
    body = (
        "Hello!\n\n"
        "This is a test email sent with Python.\n\n"
        "Best regards,\n"
        "NextGrant Team"
    )

    try:
        send_email(recipient, subject, body)
        print("Email accepted by SMTP server.")

    except smtplib.SMTPAuthenticationError:
        print("SMTP authentication failed. Check your credentials.")

    except (smtplib.SMTPException, OSError, ValueError) as exc:
        print(f"Email sending failed: {type(exc).__name__}")

if __name__ == '__main__':

    # for testing the template use any of the following
    #"registration_success",
    #"topic_notification",
    #"deadline_reminder",
    #"login_code"
    test_template("registration_success", False)