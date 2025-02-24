"""
Exposed URLs for the Message app.

This module defines the URL patterns for the MessageViewSet,
providing separate paths for each CRUD operation and custom actions.
"""

from django.urls import path

from app.messaging.controllers.ConversationViewSet import ConversationViewSet


conversation_urlpatterns = [
    path(
        "conversation/create/",
        ConversationViewSet.as_view({"post": "create"}),
        name="create",
    ),
    path(
        "conversation/admin-client-messages/",
        ConversationViewSet.as_view({"get": "get_admin_client_messages"}),
        name="admin-client-messages",
    ),
    path(
        "conversation/add-admin/",
        ConversationViewSet.as_view({"post": "add_admin_to_conversation"}),
        name="conversation-add-admin",
    ),
    path(
        "conversation/remove-admin/",
        ConversationViewSet.as_view({"post": "remove_admin_from_conversation"}),
        name="conversation-remove-admin",
    ),
    path(
        "conversation/add-self/",
        ConversationViewSet.as_view({"post": "add_self_to_conversation"}),
        name="conversation-add-self",
    ),
    path(
        "conversation/remove-self/",
        ConversationViewSet.as_view({"post": "remove_self_from_conversation"}),
        name="conversation-remove-self",
    ),
]
