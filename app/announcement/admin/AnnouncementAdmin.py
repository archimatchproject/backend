"""
Module for custom admin configurations for the Announcement model.

This module contains the AnnouncementAdmin class for customizing
the Django admin interface for the Announcement model.
"""

from django.contrib import admin

from app.announcement.models import Announcement


class AnnouncementAdmin(admin.ModelAdmin):
    """
    Custom admin options for Announcement model.

    This class provides customizations for the admin interface of
    the Announcement model in the Django admin site.
    """

    model = Announcement


# Register the admin class with the Announcement model
admin.site.register(Announcement, AnnouncementAdmin)
