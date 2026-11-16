# Python Email Notification Demo

A lightweight Python proof of concept for sending email notifications through SMTP.

The project demonstrates:

- Sending emails using Python's built-in `smtplib`
- Secure SMTP connections using SSL/TLS
- Loading credentials from environment variables
- Selecting recipients based on CSV subscriptions
- Rendering text-based email templates
- Testing functionality without sending real emails

## Requirements

- Python 3.13
- A Gmail test account with 2-Step Verification
- A Google App Password
- `python-dotenv`
- `pytest` for testing

## Installation

Navigate to the project folder `email_demo`:

```bash
cd email_demo
```


Create and activate a virtual environment:

```bash
python -m venv .venv
source .venv/bin/activate
```

Install dependencies:

```bash
python -m pip install -r requirements.txt
```

Install pytest if it is not already included in the project dependencies:

```bash
python -m pip install pytest
```

## Configuration

Create a `.env` file in the `email_demo` directory:

```dotenv
SMTP_HOST=smtp.gmail.com
SMTP_PORT=465
SMTP_USER=your-test-email@gmail.com
SMTP_PASSWORD=your-google-app-password
```

Never commit the `.env` file to version control.

The SMTP password is loaded from the environment and is not stored directly in the Python source code.

## Recipient Configuration

Recipients are stored in `recipients.csv`.

Example:

```csv
email,name,newsletter_sub,topic_a,topic_b
alice@example.com,Alice,true,true,false
bob@example.com,Bob,false,false,true
```

Use only controlled test addresses.

Each address must occur once. Subscription fields accept `true` or `false`.

The column `newsletter_sub` indicates whether a notification is wanted or not. 
The value may have `false` while individual subscriptions fields may be `true`.
A `false` value for `newsletter_sub` means no email notification should be sent to the user.

## Email Templates

Available templates:

- `registration_success`
- `topic_notification`
- `deadline_reminder`
- `login_code`

Templates are stored in the `templates/` directory and rendered using Python's `string.Template`.

The deadline reminder currently uses a manually configured number of days. Automatic scheduling is not implemented.

The login-code template is presentation-only. Secure code generation and verification are outside this demo.

## Running the Demo

Run from the `email_demo` directory:

```bash
python main.py
```

By default, the example application should run in dry-run mode, without sending messages.

Enable real email sending only after verifying the recipient list and message content.

## Running Tests

```bash
python -m pytest tests/ -v
```

Unit tests use mocked SMTP connections and temporary test data.

They do not require valid Gmail credentials or an internet connection.

## Security Notes

- SMTP uses SSL/TLS on port 465.
- Credentials are loaded from a local `.env` file.
- The `.env` file must be excluded from Git.
- Recipient and template inputs should be validated.
- Real secrets and authentication codes must not be logged.
- SMTP acceptance does not guarantee final message delivery.
- A local `.env` file is not an encrypted secret store.

## Known Limitations

This project is intended for learning and demonstration purposes.

It does not include:

- A production newsletter subscription system
- Consent management or unsubscribe handling
- Email queues or automatic retry handling
- Automatic calendar scheduling
- Real two-factor authentication
- Production delivery monitoring

For production use, additional security, privacy, delivery, and operational requirements must be implemented.

## Reusing the Email Sender

The `email_sender.py` module exposes:

```python
send_email(recipient, subject, body)
```

It can be imported into another Python application.

The calling application is responsible for choosing recipients, preparing content, and handling delivery errors.
