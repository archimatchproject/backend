"""
Module for custom admin configurations for the ArchitectSpeciality model.

This module contains the ArchitectSpecialityAdmin class for customizing
the Django admin interface for the ArchitectSpeciality model.
"""

from django.contrib import admin

from app.core.models.ArchitectSpeciality import ArchitectSpeciality


class ArchitectSpecialityAdmin(admin.ModelAdmin):
    """
    Admin options for ArchitectSpeciality model.

    This class provides customizations for the admin interface of
    the ArchitectSpeciality model in the Django admin site.
    """

    list_display = ("id", "label", "icon")
    search_fields = ("label",)


# Register the admin class with the ArchitectSpeciality model
admin.site.register(ArchitectSpeciality, ArchitectSpecialityAdmin)
