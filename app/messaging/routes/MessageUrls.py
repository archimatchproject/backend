"""
Exposed URLs for the Message app.

This module defines the URL patterns for the MessageViewSet,
providing separate paths for each CRUD operation and custom actions.
"""

from django.urls import path

from app.messaging.controllers.MessageViewSet import MessageViewSet


message_urlpatterns = [
    path(
        "message/create/",
        MessageViewSet.as_view({"post": "create"}),
        name="message-create",
    ),
    path(
        "message/user-devices/",
        MessageViewSet.as_view({"get": "user_devices"}),
        name="message-user-devices",
    ),
    path(
        "message/conversation/",
        MessageViewSet.as_view({"get": "conversation"}),
        name="message-conversation",
    ),
]
