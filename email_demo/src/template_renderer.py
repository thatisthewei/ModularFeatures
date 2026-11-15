from pathlib import Path
from string import Template

TEMPLATE_DIR = Path(__file__).parent.parent / "templates"

ALLOWED_TEMPLATES = {
    "registration_success",
    "topic_notification",
    "deadline_reminder",
    "login_code"
    # insert more late
}


def render_template(template_name: str, variables: dict[str, str | int]) -> str:
    """
    Load a text template and replace its placeholders.
    :param template_name:   name of the template to load
    :param variables:
    :return:
    """

    if template_name not in ALLOWED_TEMPLATES:
        raise ValueError(f"Unknown template {template_name}")

    template_path = TEMPLATE_DIR / f"{template_name}.txt"
    template_content = template_path.read_text(encoding="utf-8")

    template = Template(template_content)

    try:
        return template.substitute(variables)
    except KeyError as e:
        raise ValueError(f"Missing template variable: {e.args[0]}") from e


if __name__ == "__main__":

    body = render_template(
        "registration_success",
        {"name": "Admin"}
    )

    print(body)