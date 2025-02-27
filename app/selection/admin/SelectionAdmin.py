"""
Module for custom admin configurations for the Selection  model.

This module contains the Selection Admin class for customizing
the Django admin interface for the Selection  model.
"""

from django.contrib import admin

from app.selection.models import Selection


class SelectionAdmin(admin.ModelAdmin):
    """
    SelectionAdmin is a Django ModelAdmin class for managing the Selection model in the admin interface.
    Attributes:
        list_display (tuple): Specifies the fields to be displayed in the list view.
        list_filter (tuple): Specifies the fields to be used for filtering the list view.
        search_fields (tuple): Specifies the fields to be used for searching in the list view.
    """

    list_display = ("announcement", "architect", "status")
    list_filter = ("status", "announcement")
    search_fields = ("architect__user__email", "announcement__id")


admin.site.register(Selection, SelectionAdmin)
