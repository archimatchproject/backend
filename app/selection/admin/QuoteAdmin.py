"""
Module for custom admin configurations for the Quote model.

This module contains the admin class for customizing
the Django admin interface for the Quote model.
"""

from django.contrib import admin
from app.selection.models import Quote


class QuoteAdmin(admin.ModelAdmin):
    """
    Admin configuration for the Quote model.
    """
    list_display = ('id', 'selection', 'file', 'created_at')
    search_fields = ('selection__id',)
    list_filter = ('created_at',)


admin.site.register(Quote, QuoteAdmin)
