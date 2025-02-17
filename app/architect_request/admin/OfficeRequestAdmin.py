"""
Module: app.admin

Class: OfficeRequestAdmin

Description:
    Admin configuration for the OfficeRequest model. Registers the OfficeRequest model with
    the Django admin interface.
"""

from django.contrib import admin

from app.architect_request.models import OfficeRequest


class OfficeRequestAdmin(admin.ModelAdmin):
    """
    ArchitectRequest configuration for the OfficeRequest model.
    """

    model = OfficeRequest


admin.site.register(OfficeRequest, OfficeRequestAdmin)
