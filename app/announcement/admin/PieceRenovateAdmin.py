"""
Module for custom admin configurations for the PieceRenovate model.

This module contains the PieceRenovateAdmin class for customizing
the Django admin interface for the PieceRenovate model.
"""

from django.contrib import admin

from app.announcement.models.PieceRenovate import PieceRenovate


class PieceRenovateAdmin(admin.ModelAdmin):
    """
    Admin options for PieceRenovate model.

    This class provides customizations for the admin interface of
    the PieceRenovate model in the Django admin site.
    """

    list_display = ("id", "label", "icon", "number")
    search_fields = ("label",)


# Register the admin class with the PieceRenovate model
admin.site.register(PieceRenovate, PieceRenovateAdmin)
