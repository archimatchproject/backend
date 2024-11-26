"""
Exposed URLs for the Message app.

This module defines the URL patterns for the MessageViewSet,
providing separate paths for each CRUD operation and custom actions.
"""

from django.urls import path

from app.messaging.controllers.FCMDeviceViewSet import CustomFCMDeviceViewSet


device_urlpatterns = [
    path(
        "fcm-devices/create/",
        CustomFCMDeviceViewSet.as_view({"post": "create"}),
        name="message-create",
    ),
    path(
        "fcm-devices/destroy/<int:pk>/",
        CustomFCMDeviceViewSet.as_view({"delete": "destroy"}),
        name="message-create",
    )
    
]
