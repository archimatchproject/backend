"""
This module contains the URL configuration for the UnlockRequestViewSet.
list: GET /unlock-requests/
create: POST /unlock-requests/create/
accept: POST /unlock-requests/<int:pk>/accept/
refuse: POST /unlock-requests/<int:pk>/refuse/
"""

from django.urls import path
from app.selection.controllers.UnlockRequestViewSet import UnlockRequestViewSet

urlpatterns = [
    path(
        "unlock-requests/",
        UnlockRequestViewSet.as_view({"get": "list"}),
        name="unlock-requests-list",
    ),
    path(
        "unlock-requests/create/",
        UnlockRequestViewSet.as_view({"post": "create"}),
        name="unlock-requests-create",
    ),
    path(
        "unlock-requests/<int:pk>/accept/",
        UnlockRequestViewSet.as_view({"post": "accept"}),
        name="unlock-requests-accept",
    ),
    path(
        "unlock-requests/<int:pk>/refuse/",
        UnlockRequestViewSet.as_view({"post": "refuse"}),
        name="unlock-requests-refuse",
    ),
]
