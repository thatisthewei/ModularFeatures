
import smtplib
from unittest.mock import MagicMock, patch

import pytest

from src.email_sender import send_email


@pytest.fixture
def smtp_environment(monkeypatch):
    """Provide fake SMTP credentials for testing."""
    monkeypatch.setenv("SMTP_HOST", "smtp.example.com")
    monkeypatch.setenv("SMTP_PORT", "465")
    monkeypatch.setenv("SMTP_USER", "test@example.com")
    monkeypatch.setenv("SMTP_PASSWORD", "fake-app-password")


def test_send_email_success(smtp_environment):
    """Verify SMTP connection, authentication and message."""

    import ssl

    with patch("src.email_sender.smtplib.SMTP_SSL") as mock_smtp:
        smtp_connection = mock_smtp.return_value.__enter__.return_value

        send_email(
            recipient="noreply.nextgrant@gmail.com",
            subject="Test Notification",
            body="Hello me!",
        )

        # Verify the SMTP connection.
        args, kwargs = mock_smtp.call_args

        assert args == ("smtp.example.com", 465)
        assert kwargs["timeout"] == 10
        assert kwargs["context"].verify_mode is not None

        # Verify SSL-context
        context = kwargs["context"]

        assert context.verify_mode == ssl.CERT_REQUIRED
        assert context.check_hostname is True

        # Verify authentication.
        smtp_connection.login.assert_called_once_with(
            "test@example.com",
            "fake-app-password",
        )

        # Verify the email content.
        smtp_connection.send_message.assert_called_once()

        message = smtp_connection.send_message.call_args.args[0]

        assert message["From"] == "test@example.com"
        assert message["To"] == "noreply.nextgrant@gmail.com"
        assert message["Subject"] == "Test Notification"
        assert message.get_content().strip() == "Hello me!"


def test_smtp_authentication_failure(smtp_environment):
    """Verify authentication errors are propagated."""

    with patch("src.email_sender.smtplib.SMTP_SSL") as mock_smtp:
        smtp_connection = mock_smtp.return_value.__enter__.return_value

        smtp_connection.login.side_effect = (
            smtplib.SMTPAuthenticationError(
                535,
                b"Authentication failed",
            )
        )

        with pytest.raises(smtplib.SMTPAuthenticationError):
            send_email(
                "noreply.nextgrant@gmail.com",
                "Test",
                "Hello!",
            )

        smtp_connection.send_message.assert_not_called()


def test_smtp_connection_failure(smtp_environment):
    """Verify connection failures are propagated."""

    with patch("src.email_sender.smtplib.SMTP_SSL") as mock_smtp:
        mock_smtp.side_effect = OSError("Connection refused")

        with pytest.raises(OSError, match="Connection refused"):
            send_email(
                "noreply.nextgrant@gmail.com",
                "Test",
                "Hello!",
            )


def test_smtp_delivery_failure(smtp_environment):
    """Verify delivery errors are propagated."""

    with patch("src.email_sender.smtplib.SMTP_SSL") as mock_smtp:
        smtp_connection = mock_smtp.return_value.__enter__.return_value

        smtp_connection.send_message.side_effect = (
            smtplib.SMTPRecipientsRefused({
                "noreply.nextgrant@gmail.com": (550, b"Recipient rejected")
            })
        )

        with pytest.raises(smtplib.SMTPRecipientsRefused):
            send_email(
                "noreply.nextgrant@gmail.com",
                "Test",
                "Hello!",
            )

