import pytest

from src.template_renderer import render_template


def test_registration_template():
    result = render_template(
        "registration_success",
        {"name": "Admin"},
    )

    assert "Hello Admin" in result
    assert "Your registration was successful." in result


def test_topic_notification_template():
    result = render_template(
        "topic_notification",
        {
            "name": "Admin",
            "topic": "Topic A",
            "content": "New article available!",
        },
    )

    assert "Hello Admin" in result
    assert "Topic A" in result
    assert "New article available!" in result


def test_deadline_reminder_template():
    result = render_template(
        "deadline_reminder",
        {
            "name": "Admin",
            "topic": "Topic A",
            "subject": "Application deadline",
            "time": "7 days",
        },
    )

    assert "Topic A" in result
    assert "Application deadline" in result
    assert "7 days" in result


def test_login_code_template():
    result = render_template(
        "login_code",
        {
            "code": "123456",
            "expires_in_minutes": 5,
        },
    )

    assert "123456" in result
    assert "5 minutes" in result


def test_missing_template_variable():
    with pytest.raises(ValueError, match="Missing template variable"):
        render_template(
            "registration_success",
            {},
        )


def test_unknown_template():
    with pytest.raises(ValueError, match="Unknown template"):
        render_template(
            "../secrets",
            {"name": "Admin"},
        )
