"""
exposed URLS for users app
viewset : ClientViewSet
"""

from django.urls import path

from app.users.controllers import ClientViewSet


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
]
