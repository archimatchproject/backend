"""
utility functions for the selection app
"""

# from app.email_templates.tasks import send_email_background_task

from django.template.loader import render_to_string


def generate_choices(min_value: int, max_value: int, label_template: str) -> list:
    """
    Generate a list of dictionaries for choices with custom labels, values, and IDs.

    Args:
        min_value (int): Minimum value for the range.
        max_value (int): Maximum value for the range.
        label_template (str): Template string for labels with a placeholder {value}.

    Returns:
        list: A list of dictionaries with label, value, and ID.
    """
    return [
        {
            "id": idx,
            "label": label_template.format(value=value),
            "value": value,
        }
        for idx, value in enumerate(range(min_value, max_value + 1), start=1)
    ]


def send_email_with_template(to_email, subject, body, images):
    """Global function to send email with HTML template."""
    try:
        from project_core.django import base as settings
        from django.core.mail import EmailMultiAlternatives
        from app.email_templates.utils import attach_email_icons

        from_email = getattr(settings, "DEFAULT_FROM_EMAIL", "ghazichaftar@gmail.com")
        email_message = EmailMultiAlternatives(subject, body, from_email, [to_email])
        email_message.attach_alternative(body, "text/html")
        attach_email_icons(email_message, images)
        email_message.send()
    except Exception:
        raise


def send_email(data):
    """
    Sends an email using a template and handles errors gracefully.

    Args:
        data (dict): Dictionary containing:
            - 'template_name': The name of the email template.
            - 'context': The context dictionary for rendering the template.
            - 'to_email': The recipient email address.
            - 'subject': The email subject.
            - 'images': (Optional) A list of images to include in the email.
    Raises:
        Exception: If any error occurs during email sending or template rendering.
    """
    try:
        from project_core.django import base as settings

        # Extract parameters from the data dictionary
        template_name = data.get("template_name", "default_template.html")
        context = data.get("context", {})
        to_email = data.get("to_email", "default@example.com")
        subject = data.get("subject", "Default Subject")
        images = data.get("images", getattr(settings, "COMMON_IMAGES", []))

        # Render the email template
        html_content = render_to_string(template_name, context)

        # Send the email
        send_email_with_template(to_email, subject, html_content, images)
    except Exception as e:
        print(f"Task failed with error: {e}")
        from app.email_templates.tasks import send_error_email

        send_error_email(f"Task failed with error: {e}")
        raise


def send_reminder_email(announcement, email_template):
    """
    Sends a reminder email to the architect related to an announcement.

    Args:
        announcement (Announcement): The announcement instance triggering the email.
    """
    try:
        from project_core.django import base as settings

        architect = announcement.architect
        if not architect or not architect.user.email:
            print(f"No architect or email found for announcement {announcement.id}")
            return

        # Prepare the email data
        data = {
            "template_name": email_template,
            "context": {
                "first_name": architect.user.first_name,
                "last_name": architect.user.last_name,
                "email": architect.user.email,
            },
            "to_email": architect.user.email,
            "subject": "Reminder: Architect Project Selection",
            "images": getattr(settings, "REFUSE_ARCHITECT_REQUEST_IMAGES", []),
        }

        # Send the email
        send_email(data)
    except Exception as e:
        print(f"Error sending email for announcement {announcement.id}: {e}")


def send_reminder_discussion_email(selection, email_template):
    """
    Sends a reminder email to the architect related to a selection.

    Args:
        announcselectionement (Selection): The selection instance triggering the email.
    """
    try:
        from project_core.django import base as settings

        architect = selection.architect
        if not architect or not architect.user.email:
            print(f"No architect or email found for selection {selection.id}")
            return

        # Prepare the email data
        data = {
            "template_name": email_template,
            "context": {
                "first_name": architect.user.first_name,
                "last_name": architect.user.last_name,
                "email": architect.user.email,
            },
            "to_email": architect.user.email,
            "subject": "Reminder: Architect Project Selection",
            "images": getattr(settings, "REFUSE_ARCHITECT_REQUEST_IMAGES", []),
        }

        # Send the email
        send_email(data)
    except Exception as e:
        print(f"Error sending email for announcement {selection.id}: {e}")
