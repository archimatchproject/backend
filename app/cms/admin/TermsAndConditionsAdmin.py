"""
Module defining the TermsAndConditionsAdmin and related configurations.

This module contains the admin configuration for the TermsAndConditions model,
providing customization options for managing terms and conditions entries.
"""

from django.contrib import admin

from app.cms.models.TermsAndConditions import TermsAndConditions


class TermsAndConditionsAdmin(admin.ModelAdmin):
    """
    Admin descriptor for TermsAndConditions model.

    Provides options for listing, searching, and filtering
    terms and conditions entries in the Django admin interface.
    """

    list_display = ("admin", "created_at")
    list_filter = ("created_at",)


admin.site.register(TermsAndConditions, TermsAndConditionsAdmin)
