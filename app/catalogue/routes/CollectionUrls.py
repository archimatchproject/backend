"""
Exposed URLs for the Collection model.

This module defines the URL patterns for the CollectionViewSet,
providing separate paths for each CRUD operation.
"""

from django.urls import path

from app.catalogue.controllers.CollectionViewSet import CollectionViewSet


collection_urlpatterns = [
    path(
        "collection",
        CollectionViewSet.as_view({"get": "get"}),
        name="collection-list",
    ),
    path(
        "collection/create/",
        CollectionViewSet.as_view({"post": "create"}),
        name="collection-create",
    ),
    path(
        "collection/<int:pk>",
        CollectionViewSet.as_view({"get": "retrieve"}),
        name="collection-detail",
    ),
    path(
        "collection/update/<int:pk>/",
        CollectionViewSet.as_view({"put": "update"}),
        name="collection-update",
    ),
    path(
        "collection/delete/<int:pk>/",
        CollectionViewSet.as_view({"delete": "destroy"}),
        name="collection-delete",
    ),
    path(
        "collection/update-order/<int:pk>/",
        CollectionViewSet.as_view({"put": "update_order"}),
        name="collection-update-order",
    ),
    path(
        "collection/update-display-status/<int:pk>/",
        CollectionViewSet.as_view({"put": "update_display_status"}),
        name="collection-update-display-status",
    ),
    path(
        "collection/update-visibility/<int:pk>/",
        CollectionViewSet.as_view({"put": "update_visibility"}),
        name="update-visibility",
    ),
]
