"""
Module for custom admin configurations for the AnnouncementPieceRenovate model.

This module contains the AnnouncementPieceRenovateAdmin class for customizing
the Django admin interface for the AnnouncementPieceRenovate model.
"""

from django.contrib import admin

from app.announcement.models.AnnouncementPieceRenovate import AnnouncementPieceRenovate


class AnnouncementPieceRenovateAdmin(admin.ModelAdmin):
    """
    Admin options for AnnouncementPieceRenovate model.

    This class provides customizations for the admin interface of
    the AnnouncementPieceRenovate model in the Django admin site.
    """

    list_display = [
        "announcement",
        "piece_renovate",
        "number",
    ]
    search_fields = ("piece_renovate",)


# Register the admin class with the AnnouncementPieceRenovate model
admin.site.register(
    AnnouncementPieceRenovate,
    AnnouncementPieceRenovateAdmin,
)
