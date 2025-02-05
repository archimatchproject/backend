"""
Module defining the CGUCGVPolicyAdmin and related configurations.

This module contains the admin configuration for the CGUCGVPolicy model,
providing customization options for managing CGUCGV policy entries.
"""

from django.contrib import admin

from app.cms.models.CGUCGVPolicy import CGUCGVPolicy


class CGUCGVPolicyAdmin(admin.ModelAdmin):
    """
    Admin descriptor for CGUCGVPolicy model.

    Provides options for listing, searching, and filtering
    CGUCGV policy entries in the Django admin interface.
    """

    list_display = ("admin", "created_at")
    list_filter = ("created_at",)


admin.site.register(CGUCGVPolicy, CGUCGVPolicyAdmin)
