"""
Module for custom admin configurations for the ArchitecturalStyle model.

This module contains the ArchitecturalStyleAdmin class for customizing
the Django admin interface for the ArchitecturalStyle model.
"""

from django.contrib import admin

from app.core.models.ArchitecturalStyle import ArchitecturalStyle


class ArchitecturalStyleAdmin(admin.ModelAdmin):
    """
    Admin options for ArchitecturalStyle model.

    This class provides customizations for the admin interface of
    the ArchitecturalStyle model in the Django admin site.
    """

    list_display = ("id", "label", "icon")
    search_fields = ("label",)


# Register the admin class with the ArchitecturalStyle model
admin.site.register(ArchitecturalStyle, ArchitecturalStyleAdmin)
