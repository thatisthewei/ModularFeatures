import pytest
import src.recipients as recipients
from src.recipients import get_recipients_by_topic

def test_invalid_subscription_value(tmp_path, monkeypatch):
    csv_file = tmp_path / "recipients.csv"

    csv_file.write_text(
        "email,name,topic_a,topic_b\n"
        "alice@example.com,Alice,yes,false\n",
        encoding="utf-8",
    )

    monkeypatch.setattr(recipients, "CSV_PATH", csv_file)

    with pytest.raises(ValueError, match="Invalid subscription"):
        recipients.get_recipients_by_topic("topic_a")


def test_invalid_email_address(tmp_path, monkeypatch):
    csv_file = tmp_path / "recipients.csv"

    csv_file.write_text(
        "email,name,topic_a,topic_b\n"
        "not-an-email,Alice,true,false\n",
        encoding="utf-8",
    )

    monkeypatch.setattr(recipients, "CSV_PATH", csv_file)

    with pytest.raises(ValueError, match="Invalid email"):
        recipients.get_recipients_by_topic("topic_a")


def test_topic_a_recipients():
    recipients = get_recipients_by_topic("topic_a")

    names = {recipient["name"] for recipient in recipients}

    assert names == {"Admin", "Wei"}


def test_topic_b_recipients():
    recipients = get_recipients_by_topic("topic_b")

    names = {recipient["name"] for recipient in recipients}

    assert names == {"Admin", "Marc"}


def test_unknown_topic():
    import pytest

    with pytest.raises(ValueError):
        get_recipients_by_topic("unknown_topic")