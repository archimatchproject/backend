"""
Utility functions for sending HTML template emails with embedded images.

This module provides functions to send HTML emails using Django's
EmailMultiAlternatives class.
It includes functionality to attach images inline within the HTML content of the email.
"""

import os

from email.mime.image import MIMEImage

from django.core.mail import EmailMultiAlternatives

from project_core.django import base as settings


def send_email_with_template(to_email, subject, body, images):
    """Global function to send email with HTML template."""
    try:
        from_email = settings.DEFAULT_FROM_EMAIL
        email_message = EmailMultiAlternatives(subject, body, from_email, [to_email])
        email_message.attach_alternative(body, "text/html")
        attach_email_icons(email_message, images)
        email_message.send()
    except Exception:
        raise


def attach_email_icons(msg, images):
    """Attach icons to email template."""
    msg.mixed_subtype = "related"

    for path, filename in images:
        with open(os.path.join(path, filename), "rb") as f:
            img = MIMEImage(f.read())

        # Define the content ID
        img.add_header("Content-ID", f"<{filename}>")
        img.add_header("Content-Disposition", "inline", filename=filename)

        msg.attach(img)
