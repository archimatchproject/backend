"""
Exposed URLs for the Product model.

This module defines the URL patterns for the ProductViewSet,
providing separate paths for each CRUD operation.
"""

from django.urls import path

from app.catalogue.controllers.ProductViewSet import ProductViewSet


product_urlpatterns = [
    path(
        "product",
        ProductViewSet.as_view({"get": "list"}),
        name="product-list",
    ),
    path(
        "product/create/",
        ProductViewSet.as_view({"post": "create"}),
        name="product-create",
    ),
    path(
        "product/<int:pk>",
        ProductViewSet.as_view({"get": "retrieve"}),
        name="product-detail",
    ),
    path(
        "product/update/<int:pk>/",
        ProductViewSet.as_view({"put": "update"}),
        name="product-update",
    ),
    path(
        "product/delete/<int:pk>/",
        ProductViewSet.as_view({"delete": "destroy"}),
        name="product-delete",
    ),
    path(
        "product/update-display-status/<int:pk>/",
        ProductViewSet.as_view({"put": "update_display_status"}),
        name="product-update-display-status",
    ),
    path(
        "product/update-visibility/<int:pk>/",
        ProductViewSet.as_view({"put": "update_visibility"}),
        name="update-visibility",
    ),
]
