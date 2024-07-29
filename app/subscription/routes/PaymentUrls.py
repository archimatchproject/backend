"""
Exposed URLs for the Payment model.

This module defines the URL patterns for the PaymentViewSet,
providing separate paths for each CRUD operation.
"""

from django.urls import path

from app.subscription.controllers.PaymentViewSet import PaymentViewSet


payment_urlpatterns = [
    path(
        "payment",
        PaymentViewSet.as_view({"get": "list"}),
        name="payment-list",
    ),
    path(
        "payment/create/",
        PaymentViewSet.as_view({"post": "create"}),
        name="payment-create",
    ),
    path(
        "payment/<int:pk>",
        PaymentViewSet.as_view({"get": "retrieve"}),
        name="payment-detail",
    ),
    path(
        "payment/update/<int:pk>/",
        PaymentViewSet.as_view({"put": "update"}),
        name="payment-update",
    ),
    path(
        "payment/delete/<int:pk>/",
        PaymentViewSet.as_view({"delete": "destroy"}),
        name="payment-delete",
    ),
    path(
        "payment/methods",
        PaymentViewSet.as_view({"get": "get_payment_methods"}),
        name="payment-methods",
    ),
]
