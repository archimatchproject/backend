"""
Module for custom admin configurations for the Realization model.

This module contains the RealizationAdmin class for customizing
the Django admin interface for the Realization model.
"""

from django.contrib import admin

from app.architect_realization.models.Realization import Realization


class RealizationAdmin(admin.ModelAdmin):
    """
    Custom admin options for Realization model.

    This class provides customizations for the admin interface of
    the Realization model in the Django admin site.
    """

    model = Realization


# Register the admin class with the Realization model
admin.site.register(Realization, RealizationAdmin)
