"""
Exposed URLs for the Payment model.

This module defines the URL patterns for the PaymentViewSet,
providing separate paths for each CRUD operation.
"""

from django.urls import path

from app.subscription.controllers.EventDiscountViewSet import EventDiscountViewSet


event_discount_urlpatterns = [
    path(
        "event-discount",
        EventDiscountViewSet.as_view({"get": "list"}),
        name="event-discount-list",
    ),
    path(
        "event-discount/create/",
        EventDiscountViewSet.as_view({"post": "create"}),
        name="event-discount-create",
    ),
    path(
        "event-discount/<int:pk>",
        EventDiscountViewSet.as_view({"get": "retrieve"}),
        name="event-discount-detail",
    ),
    path(
        "event-discount/update/<int:pk>/",
        EventDiscountViewSet.as_view({"put": "update"}),
        name="event-discount-update",
    ),
    path(
        "event-discount/delete/<int:pk>/",
        EventDiscountViewSet.as_view({"delete": "destroy"}),
        name="event-discount-delete",
    ),
    path(
        "event-discount/get-active-discount/",
        EventDiscountViewSet.as_view({"get": "get_active_event_discount"}),
        name="get-active-discount",
    ),
]
