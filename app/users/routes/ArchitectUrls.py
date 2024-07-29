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
    path(
        "architect/get-profile/",
        ArchitectViewSet.as_view({"get": "architect_get_profile"}),
        name="profile",
    ),
    path(
        "architect/update-base-details/",
        ArchitectViewSet.as_view({"post": "architect_update_base_details"}),
        name="update-base-details",
    ),
    path(
        "architect/update-company-details/",
        ArchitectViewSet.as_view({"post": "architect_update_company_details"}),
        name="update-company-details",
    ),
    path(
        "architect/update-needs/",
        ArchitectViewSet.as_view({"post": "architect_update_needs"}),
        name="update-needs",
    ),
]
