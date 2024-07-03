"""
Module for custom admin configurations for the WorkType model.

This module contains the WorkTypeAdmin class for customizing
the Django admin interface for the WorkType model.
"""

from django.contrib import admin

from app.core.models.WorkType import WorkType


class WorkTypeAdmin(admin.ModelAdmin):
    """
    Admin options for WorkType model.

    This class provides customizations for the admin interface of
    the WorkType model in the Django admin site.
    """

    list_display = ("id", "header", "description")
    search_fields = ("header",)


# Register the admin class with the WorkType model
admin.site.register(WorkType, WorkTypeAdmin)
