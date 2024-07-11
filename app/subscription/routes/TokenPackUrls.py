"""
Exposed URLs for the TokenPack model.

This module defines the URL patterns for the TokenPackViewSet,
providing separate paths for each CRUD operation.
"""

from django.urls import path

from app.subscription.controllers.TokenPackViewSet import TokenPackViewSet


token_pack_urlpatterns = [
    path(
        "token-pack",
        TokenPackViewSet.as_view({"get": "list"}),
        name="token-pack-list",
    ),
    path(
        "token-pack/create/",
        TokenPackViewSet.as_view({"post": "create"}),
        name="token-pack-create",
    ),
    path(
        "token-pack/<int:pk>",
        TokenPackViewSet.as_view({"get": "retrieve"}),
        name="token-pack-detail",
    ),
    path(
        "token-pack/update/<int:pk>/",
        TokenPackViewSet.as_view({"put": "update"}),
        name="token-pack-update",
    ),
    path(
        "token-pack/delete/<int:pk>/",
        TokenPackViewSet.as_view({"delete": "destroy"}),
        name="token-pack-delete",
    ),
]
