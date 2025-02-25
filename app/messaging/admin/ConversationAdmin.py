"""
Admin module for the Message model.

This module defines the admin interface configuration for the Message model,
allowing for management of message instances via the Django admin interface.
"""

from django.contrib import admin

from app.messaging.models.Conversation import Conversation


class ConversationAdmin(admin.ModelAdmin):
    """
    Admin interface configuration for the Message model.

    """

    list_display = ("user",)


admin.site.register(Conversation, ConversationAdmin)
