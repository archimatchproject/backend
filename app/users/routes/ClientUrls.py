"""
exposed URLS for users app
viewset : ClientViewSet
"""

from django.urls import path

from app.users.controllers.ClientViewSet import ClientViewSet


client_urlpatterns = [
    path(
        "client/login-email/",
        ClientViewSet.as_view({"post": "client_login_email"}),
        name="login-email",
    ),
    path(
        "client/send-reset-password-link/",
        ClientViewSet.as_view({"post": "client_send_reset_password_link"}),
        name="send-reset-password-link",
    ),
    path(
        "client/validate-password-token/",
        ClientViewSet.as_view({"post": "client_validate_password_token"}),
        name="validate-password-token",
    ),
    path(
        "client/validate-email-token/",
        ClientViewSet.as_view({"post": "client_validate_email_token"}),
        name="validate-email-token",
    ),
]
