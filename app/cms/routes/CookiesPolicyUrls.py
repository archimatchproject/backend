"""
Exposed URLs for the CookiesPolicy viewset.

This module defines the URL patterns for the CookiesPolicyViewSet,
providing separate paths for each CRUD operation.
"""

from django.urls import path

from app.cms.controllers.CookiesPolicyViewSet import CookiesPolicyViewSet


cookies_policy_urlpatterns = [
    path(
        "cookies-policy",
        CookiesPolicyViewSet.as_view({"get": "list"}),
        name="cookies-policy-list",
    ),
    path(
        "cookies-policy/create/",
        CookiesPolicyViewSet.as_view({"post": "create"}),
        name="cookies-policy-create",
    ),
    path(
        "cookies-policy/<int:pk>",
        CookiesPolicyViewSet.as_view({"get": "retrieve"}),
        name="cookies-policy-detail",
    ),
    path(
        "cookies-policy/update/<int:pk>/",
        CookiesPolicyViewSet.as_view({"put": "update"}),
        name="cookies-policy-update",
    ),
    path(
        "cookies-policy/delete/<int:pk>/",
        CookiesPolicyViewSet.as_view({"delete": "destroy"}),
        name="cookies-policy-delete",
    ),
    path(
        "cookies-policy/get-by-admin",
        CookiesPolicyViewSet.as_view({"get": "get_policy_by_admin"}),
        name="cgu-cgv-policy-by-admin",
    ),
]
