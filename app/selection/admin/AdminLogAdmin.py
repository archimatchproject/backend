"""
This module configures the Django admin interface for the ActionLog model.
It customizes how logs are displayed, searched, and filtered in the admin panel.
"""

from django.contrib import admin

from app.selection.models.ActionLog import ActionLog


class ActionLogAdmin(admin.ModelAdmin):
    """
    Admin configuration for the ActionLog model.
    Provides customizations for list display, filtering, and search functionality.
    """

    list_display = ("admin", "action", "timestamp", "formatted_details")
    list_filter = ("action", "timestamp")
    search_fields = ("admin__user__first_name", "action", "details")
    ordering = ("-timestamp",)
    # readonly_fields = ('user', 'action', 'timestamp', 'details')

    def formatted_details(self, obj):
        """
        Display a readable version of the details JSON field.

        :param obj: The ActionLog instance being displayed.
        :return: A string representation of the details field.
        """
        if obj.details:
            return ", ".join([f"{key}: {value}" for key, value in obj.details.items()])
        return "No details"

    formatted_details.short_description = "Details"


admin.site.register(ActionLog, ActionLogAdmin)
