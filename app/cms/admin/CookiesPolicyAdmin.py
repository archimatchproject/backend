"""
Module defining the CookiesPolicyAdmin and related configurations.

This module contains the admin configuration for the CookiesPolicy model,
providing customization options for managing Cookies policy entries.
"""

from django.contrib import admin

from app.cms.models.CookiesPolicy import CookiesPolicy


class CookiesPolicyAdmin(admin.ModelAdmin):
    """
    Admin descriptor for CookiesPolicy model.

    Provides options for listing, searching, and filtering
    Cookies policy entries in the Django admin interface.
    """

    list_display = ("admin", "created_at")
    list_filter = ("created_at",)


admin.site.register(CookiesPolicy, CookiesPolicyAdmin)
