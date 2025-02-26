"""
Module: app.admin

Classes:
- UnitAdmin: Admin configuration for the Unit model.

Description:
This module registers the Unit model with the Django admin interface
and defines custom configurations for managing the Unit model.
"""

from django.contrib import admin

from app.quote.models.Unit import Unit


class UnitAdmin(admin.ModelAdmin):
    """
    Admin configuration for the Unit model.

    Attributes:
    - model: Specifies the Unit model.
    - list_display: Defines the fields to be displayed in the list view of the admin interface.
    - search_fields: Specifies which fields should be searchable in the admin interface.
    """

    model = Unit
    list_display = ("id", "title", "created_at", "updated_at")
    search_fields = ("title",)


admin.site.register(Unit, UnitAdmin)
