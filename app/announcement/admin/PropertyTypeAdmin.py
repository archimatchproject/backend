"""
Module for custom admin configurations for the PropertyType model.

This module contains the PropertyTypeAdmin class for customizing
the Django admin interface for the PropertyType model.
"""

from django.contrib import admin

from app.announcement.models.PropertyType import PropertyType


class PropertyTypeAdmin(admin.ModelAdmin):
    """
    Admin options for PropertyType model.

    This class provides customizations for the admin interface of
    the PropertyType model in the Django admin site.
    """

    list_display = (
        "id",
        "label",
        "icon",
        "project_category",
    )
    search_fields = ("label",)
    list_filter = ("project_category",)


# Register the admin class with the PropertyType model
admin.site.register(PropertyType, PropertyTypeAdmin)
