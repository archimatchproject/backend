"""
Module for custom admin configurations for the SoftwareSkill model.

This module contains the SoftwareSkillAdmin class for customizing
the Django admin interface for the SoftwareSkill model.
"""

from django.contrib import admin

from app.officeOffer.models import SoftwareSkill


class SoftwareSkillAdmin(admin.ModelAdmin):
    """
    Custom admin options for SoftwareSkill model.

    This class provides customizations for the admin interface of
    the SoftwareSkill model in the Django admin site.
    """

    model = SoftwareSkill


# Register the admin class with the SoftwareSkill model
admin.site.register(SoftwareSkill, SoftwareSkillAdmin)
