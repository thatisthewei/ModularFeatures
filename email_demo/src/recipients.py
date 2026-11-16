import pandas as pd
from pathlib import Path

from src.email_sender import send_email

from email.utils import parseaddr

# you may also write in the total path to the file
CSV_PATH = Path(__file__).resolve().parent.parent / "recipients.csv"
# if needed, limit the topics, where email should be sent for
ALLOWED_TOPICS = {"topic_a", "topic_b"}  # change for actual topics

NOTIFICATION_TEMPLATE = Path(__file__).resolve().parent / "topic_notification.txt"


def is_valid_email(email: str) -> bool:
    """Perform basic validation of a demo email address."""

    if not email or any(char.isspace() for char in email):
        return False

    if "\r" in email or "\n" in email:
        return False

    _, parsed_address = parseaddr(email, strict=True)

    if parsed_address != email:
        return False

    local_part, separator, domain = email.partition("@")

    return (
        separator == "@"
        and bool(local_part)
        and "." in domain
        and not domain.startswith(".")
        and not domain.endswith(".")
    )


def get_recipients_by_topic(topic: str) -> list[dict[str, str]]:
    """Return recipients subscribed to the specified topic."""

    if topic not in ALLOWED_TOPICS:
        raise ValueError(f"Unknown topic: {topic}")

    recipients = []
    seen_emails = set()

    # change separator if needed ',', ';', etc.
    recipients_df = pd.read_csv(CSV_PATH, sep=',')
    # print(recipients_df.head())
    if (len(recipients_df) == 0 or recipients_df.empty
            or not {"email", "name"}.issubset(recipients_df.columns)):
        raise ValueError("Invalid recipient CSV columns.")

    for i in range(0, len(recipients_df)):
        row = recipients_df.iloc[i]
        #print(row)

        for column in ALLOWED_TOPICS:
            value = row[column]

            if value not in {False, True}:
                raise ValueError(
                    f"Invalid subscription value in column: {column}"
                )

        # skip row if newsletter are not requested in general
        if not row["newsletter_sub"]:
            continue
        email = (row["email"] or "").strip().lower()
        name = (row["name"] or "").strip()
        subscription = row[topic]

        if not email or not name:
            continue

        if not is_valid_email(email):
            print(f"Invalid email address in recipients.csv.")
            print(f"Code will continue, but will skip this email {email}")
            # input("Press Enter to continue...")
            continue

        if not subscription:
            continue

        if email in seen_emails:
            continue

        recipients.append({
            "email": email,
            "name": name
        })
        seen_emails.add(email)
    return recipients


def test_recipients():
    # replace with actual topic
    topic = "topic_a"
    send_messages = False

    recipients = get_recipients_by_topic(topic)
    print(f"Recipients subscribed to {topic}:")

    for recipient in recipients:
        print(f"- {recipient['name']}: {recipient['email']}")

        subject = f"New notification for {topic}"

        body = (
            f"Hello {recipient['name']},\n\n"
            f"There is a new update about {topic}.\n\n"
            "Best regards,\n"
            "The NextGrant Team"
        )

        print(f"Recipient: {recipient['email']}")

        if send_messages:
            send_email(recipient=recipient["email"], subject=subject, body=body)

    print(f"\nProcessed: {len(recipients)} recipients.")

if __name__ == "__main__":
    test_recipients()