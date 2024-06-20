"""
Module for custom admin configurations for the ProjectExtension model.

This module contains the ProjectExtensionAdmin class for customizing
the Django admin interface for the ProjectExtension model.
"""

from django.contrib import admin

from app.announcement.models.ProjectExtension import ProjectExtension


class ProjectExtensionAdmin(admin.ModelAdmin):
    """
    Admin options for ProjectExtension model.

    This class provides customizations for the admin interface of
    the ProjectExtension model in the Django admin site.
    """

    list_display = ("id", "label", "icon")
    search_fields = ("label",)


# Register the admin class with the ProjectExtension model
admin.site.register(ProjectExtension, ProjectExtensionAdmin)
