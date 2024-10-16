"""
Admin registration module for the Warning model.
"""

from django.contrib import admin

from app.moderation.models.Warning import Warning


class WarningAdmin(admin.ModelAdmin):
    """
    Admin interface for Warning.
    """

    list_display = ("issued_by", "issued_for", "created_at")
    search_fields = ("issued_by__user__email", "issued_for__email")
    list_filter = ("created_at",)


admin.site.register(Warning, WarningAdmin)
