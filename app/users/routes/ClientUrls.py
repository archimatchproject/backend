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
        "client/send-code/",
        ClientViewSet.as_view({"post": "client_send_verification_code"}),
        name="send-code",
    ),
    path(
        "client/verify-code/",
        ClientViewSet.as_view({"post": "client_verify_verification_code"}),
        name="verify-code",
    ),
    path(
        "client/send-reset-password-link/",
        ClientViewSet.as_view({"post": "client_send_reset_password_link"}),
        name="send-reset-password-link",
    ),
]
