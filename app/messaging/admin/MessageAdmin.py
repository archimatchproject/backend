"""
Admin module for the Message model.

This module defines the admin interface configuration for the Message model,
allowing for management of message instances via the Django admin interface.
"""

from django.contrib import admin

from app.messaging.models.Message import Message


class MessageAdmin(admin.ModelAdmin):
    """
    Admin interface configuration for the Message model.

    """

    list_display = (
        "sender_device",
        "recipient_device",
        "content",
        "timestamp",
    )


admin.site.register(Message, MessageAdmin)
