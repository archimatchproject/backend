"""
Simple view to test the email sending
"""

from django.shortcuts import render
from django.template.loader import render_to_string

from project_core.django import base

from .utils import send_email_with_template


def home(request):
    """
    view when triggered will send an email example
    """
    html_content = render_to_string(
        template_name="architect_request.html", context={"reset_link": "google.com"}
    )
    send_email_with_template(
        "ghazichaftar.pfe@gmail.com", "Architect Account Creation", html_content, base.COMMON_IMAGES
    )
    return render(request, "architect_request.html")
