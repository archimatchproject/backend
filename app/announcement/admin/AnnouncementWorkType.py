"""
Module for custom admin configurations for the AnnouncementWorkType model.

This module contains the AnnouncementWorkTypeAdmin class for customizing
the Django admin interface for the AnnouncementWorkType model.
"""

from django.contrib import admin

from app.announcement.models.AnnouncementWorkType import AnnouncementWorkType


class AnnouncementWorkTypeAdmin(admin.ModelAdmin):
    """
    Admin options for AnnouncementWorkType model.

    This class provides customizations for the admin interface of
    the AnnouncementWorkType model in the Django admin site.
    """

    list_display = ("id", "header", "description")
    search_fields = ("header",)


# Register the admin class with the AnnouncementWorkType model
admin.site.register(
    AnnouncementWorkType,
    AnnouncementWorkTypeAdmin,
)
