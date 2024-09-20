"""
Exposed URLs for the CGUCGVPolicy viewset.

This module defines the URL patterns for the CGUCGVPolicyViewSet,
providing separate paths for each CRUD operation.
"""

from django.urls import path
from app.cms.controllers.CGUCGVPolicyViewSet import CGUCGVPolicyViewSet


cgu_cgv_urlpatterns = [
    path(
        "cgu-cgv-policy",
        CGUCGVPolicyViewSet.as_view({"get": "list"}),
        name="cgu-cgv-policy-list",
    ),
    path(
        "cgu-cgv-policy/create/",
        CGUCGVPolicyViewSet.as_view({"post": "create"}),
        name="cgu-cgv-policy-create",
    ),
    path(
        "cgu-cgv-policy/<int:pk>",
        CGUCGVPolicyViewSet.as_view({"get": "retrieve"}),
        name="cgu-cgv-policy-detail",
    ),
    path(
        "cgu-cgv-policy/update/<int:pk>/",
        CGUCGVPolicyViewSet.as_view({"put": "update"}),
        name="cgu-cgv-policy-update",
    ),
    path(
        "cgu-cgv-policy/delete/<int:pk>/",
        CGUCGVPolicyViewSet.as_view({"delete": "destroy"}),
        name="cgu-cgv-policy-delete",
    ),
]
