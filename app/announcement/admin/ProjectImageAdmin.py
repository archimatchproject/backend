"""
Module for custom admin configurations for the ProjectImage model.

This module contains the ProjectImageAdmin class for customizing
the Django admin interface for the ProjectImage model.
"""

from django.contrib import admin

from app.announcement.models.ProjectImage import ProjectImage


class ProjectImageAdmin(admin.ModelAdmin):
    """
    Admin options for ProjectImage model.

    This class provides customizations for the admin interface of
    the ProjectImage model in the Django admin site.
    """

    list_display = ("id", "image")


# Register the admin class with the ProjectImage model
admin.site.register(ProjectImage, ProjectImageAdmin)
