"""
Module for custom admin configurations for the ProjectCategory model.

This module contains the ProjectCategoryAdmin class for customizing
the Django admin interface for the ProjectCategory model.
"""

from django.contrib import admin

from app.core.models.ProjectCategory import ProjectCategory


class ProjectCategoryAdmin(admin.ModelAdmin):
    """
    Admin options for ProjectCategory model.

    This class provides customizations for the admin interface of
    the ProjectCategory model in the Django admin site.
    """

    list_display = ("id", "label", "icon")
    search_fields = ("label",)


# Register the admin class with the ProjectCategory model
admin.site.register(ProjectCategory, ProjectCategoryAdmin)
