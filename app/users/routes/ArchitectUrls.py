"""
exposed URLS for users app
viewset : AdminViewSet
"""

from django.urls import path

from app.users.controllers.ArchitectViewSet import ArchitectViewSet


architect_urlpatterns = [
    path(
        "architect/send-reset-password-link/",
        ArchitectViewSet.as_view({"post": "architect_send_reset_password_link"}),
        name="send-reset-password-link",
    ),
    path(
        "architect/validate-password-token/",
        ArchitectViewSet.as_view({"post": "architect_validate_password_token"}),
        name="validate-password-token",
    ),
]
