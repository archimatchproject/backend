"""
Module: app.admin

Class: ArchitectRequestAdmin

Description:
    Admin configuration for the ArchitectRequest model. Registers the ArchitectRequest model with the Django admin interface.
"""
from django.contrib import admin

from app.architect_request.models import ArchitectRequest


class ArchitectRequestAdmin(admin.ModelAdmin):

    """
    ArchitectRequest configuration for the ArchitectRequest model.
    """

    model = ArchitectRequest


admin.site.register(ArchitectRequest, ArchitectRequestAdmin)
