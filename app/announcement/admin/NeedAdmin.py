"""
Module for custom admin configurations for the Need model.

This module contains the NeedAdmin class for customizing
the Django admin interface for the Need model.
"""

from django.contrib import admin

from app.announcement.models.Need import Need


class NeedAdmin(admin.ModelAdmin):
    """
    Admin options for Need model.

    This class provides customizations for the admin interface of
    the Need model in the Django admin site.
    """

    list_display = ("id", "label", "icon", "architect_speciality")
    search_fields = ("label",)
    list_filter = ("architect_speciality",)


# Register the admin class with the Need model
admin.site.register(Need, NeedAdmin)
