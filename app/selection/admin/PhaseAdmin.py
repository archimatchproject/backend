"""
Module for custom admin configurations for the Phase model.

This module contains the admin class for customizing
the Django admin interface for the Phase model.
"""

from django.contrib import admin
from app.selection.models import Phase


class PhaseAdmin(admin.ModelAdmin):
    """
    Admin configuration for the Phase model.
    """
    list_display = ('id', 'name', 'number', 'start_date', 'limit_date')
    search_fields = ('name',)
    list_filter = ('number',)


admin.site.register(Phase, PhaseAdmin)
