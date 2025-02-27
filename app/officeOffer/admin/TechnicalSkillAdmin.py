"""
Module for custom admin configurations for the TechnicalSkill model.

This module contains the TechnicalSkillAdmin class for customizing
the Django admin interface for the TechnicalSkill model.
"""

from django.contrib import admin

from app.officeOffer.models import TechnicalSkill


class TechnicalSkillAdmin(admin.ModelAdmin):
    """
    Custom admin options for TechnicalSkill model.

    This class provides customizations for the admin interface of
    the TechnicalSkill model in the Django admin site.
    """

    model = TechnicalSkill


# Register the admin class with the TechnicalSkill model
admin.site.register(TechnicalSkill, TechnicalSkillAdmin)
