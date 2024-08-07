"""
Exposed URLs for the PrivacyPolicy viewset.

This module defines the URL patterns for the PrivacyPolicyViewSet,
providing separate paths for each CRUD operation.
"""

from django.urls import path

from app.cms.controllers.PrivacyPolicyViewSet import PrivacyPolicyViewSet


privacy_policy_urlpatterns = [
    path(
        "privacy-policy",
        PrivacyPolicyViewSet.as_view({"get": "list"}),
        name="privacy-policy-list",
    ),
    path(
        "privacy-policy/create/",
        PrivacyPolicyViewSet.as_view({"post": "create"}),
        name="privacy-policy-create",
    ),
    path(
        "privacy-policy/<int:pk>",
        PrivacyPolicyViewSet.as_view({"get": "retrieve"}),
        name="privacy-policy-detail",
    ),
    path(
        "privacy-policy/update/<int:pk>/",
        PrivacyPolicyViewSet.as_view({"put": "update"}),
        name="privacy-policy-update",
    ),
    path(
        "privacy-policy/delete/<int:pk>/",
        PrivacyPolicyViewSet.as_view({"delete": "destroy"}),
        name="privacy-policy-delete",
    ),
]
