"""
Module for custom admin configurations for the RealizationImage model.

This module contains the RealizationImageAdmin class for customizing
the Django admin interface for the RealizationImage model.
"""

from django.contrib import admin

from app.architect_realization.models.RealizationImage import RealizationImage


class RealizationImageAdmin(admin.ModelAdmin):
    """
    Admin options for RealizationImage model.

    This class provides customizations for the admin interface of
    the RealizationImage model in the Django admin site.
    """

    list_display = ("id", "image")


# Register the admin class with the RealizationImage model
admin.site.register(RealizationImage, RealizationImageAdmin)
