"""
Module for custom admin configurations for the Selection  model.

This module contains the Selection Admin class for customizing
the Django admin interface for the Selection  model.
"""

from django.contrib import admin
from app.selection.models import Selection


class SelectionAdmin(admin.ModelAdmin):
    list_display = ('announcement', 'architect', 'status')
    list_filter = ('status', 'announcement')
    search_fields = ('architect__user__email', 'announcement__id')


admin.site.register(Selection, SelectionAdmin)
