"""
Module defining the PrivacyPolicyAdmin and related configurations.

This module contains the admin configuration for the PrivacyPolicy model,
providing customization options for managing privacy policy entries.
"""

from django.contrib import admin

from app.cms.models.PrivacyPolicy import PrivacyPolicy


class PrivacyPolicyAdmin(admin.ModelAdmin):
    """
    Admin descriptor for PrivacyPolicy model.

    Provides options for listing, searching, and filtering
    privacy policy entries in the Django admin interface.
    """

    list_display = ("admin", "created_at")
    list_filter = ("created_at",)


admin.site.register(PrivacyPolicy, PrivacyPolicyAdmin)
