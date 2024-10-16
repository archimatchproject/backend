"""
Module for handling background tasks related to email sending
"""

from django.core.mail import send_mail
from django.template.loader import render_to_string

from background_task import background

from project_core.django import base as settings

from .utils import send_email_with_template


@background(schedule=0)
def send_email_background_task(data):
    """
    Background task to send an email using a template and handle errors gracefully.
    Args:
        data (dict): Dictionary containing 'template_name', 'context', 'to_email', 'subject',
        and 'images'.
    Raises:
        Exception: If any error occurs during email sending or template rendering.
    """
    try:
        template_name = data.get("template_name", "default_template.html")
        context = data.get("context", {})
        to_email = data.get("to_email", "default@example.com")
        subject = data.get("subject", "Default Subject")
        images = data.get("images", settings.COMMON_IMAGES)
        print(to_email)
        html_content = render_to_string(template_name=template_name, context=context)

        send_email_with_template(to_email, subject, html_content, images)
    except Exception as e:
        print(f"Task failed with error: {e}")
        send_error_email(f"Task failed with error: {e}")
        raise


def send_error_email(error_message):
    """
    Sends an error email notification.

    Args:
        error_message (str): Error message to include in the email body.

    """
    try:
        send_mail(
            "Error in Background Task",
            error_message,
            settings.DEFAULT_FROM_EMAIL,
            [settings.EMAIL_HOST_USER],
            fail_silently=False,
        )
    except Exception as e:
        print(f"Failed to send error email: {e}")
