"""
exposed URLS for users app
viewset : OfficeViewSet
"""

from django.urls import path

from app.users.controllers.OfficeViewSet import OfficeViewSet


office_urlpatterns = [
    path(
        "office/signup/",
        OfficeViewSet.as_view({"post": "office_signup"}),
        name="signup",
    ),
    path(
        "office/login/",
        OfficeViewSet.as_view({"post": "office_login"}),
        name="login",
    ),
    path(
        "office/get-all-offices/",
        OfficeViewSet.as_view({"get": "get"}),
        name="get-all-offices",
    ),
    path(
        "offices/delete/<int:pk>/",
        OfficeViewSet.as_view({"delete": "delete"}),
        name="delete-office",
    ),
    path(
        "office/validate-password-token/",
        OfficeViewSet.as_view({"post": "office_validate_password_token"}),
        name="validate-password-token",
    ),
    path(
        "office/resend-email/<int:pk>/",
        OfficeViewSet.as_view({"post": "office_resend_email"}),
        name="resend-email",
    ),
    path(
        "office/first-connection/",
        OfficeViewSet.as_view({"post": "office_first_cnx"}),
        name="first-connection",
    ),
]
