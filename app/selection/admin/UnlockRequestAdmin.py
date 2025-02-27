"""
Admin configuration for the UnlockRequest model.

This module contains the admin configuration for the UnlockRequest model,
including the following classes:

Classes:
    UnlockRequestAdmin: Customizes the admin interface for UnlockRequest instances.
"""

from django.contrib import admin

from app.selection.models.UnlockRequest import UnlockRequest


class UnlockRequestAdmin(admin.ModelAdmin):
    """
    Admin configuration for the UnlockRequest model.

    This class customizes the admin interface for UnlockRequest instances,
    including the fields to be displayed, search fields, and list filters.

    Attributes:
        list_display (tuple): Fields to be displayed in the list view.
        search_fields (tuple): Fields to be searched in the admin interface.
        list_filter (tuple): Fields to filter the list view.
    """

    list_display = ("selection", "status", "message")
    search_fields = ("selection__name", "status")
    list_filter = ("status",)

    def __str__(self):
        """
        Returns a string representation of the UnlockRequestAdmin instance.
        """
        return f"UnlockRequestAdmin for {self.selection.name} - {self.status}"


admin.site.register(UnlockRequest, UnlockRequestAdmin)
