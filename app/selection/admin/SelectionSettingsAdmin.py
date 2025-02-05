"""
Module for custom admin configurations for the SelectionSettings model.

This module contains the admin class for customizing
the Django admin interface for the SelectionSettings model.
"""

from django.contrib import admin
from app.selection.models import SelectionSettings


class SelectionSettingsAdmin(admin.ModelAdmin):
    """
    Admin configuration for the SelectionSettings model.
    """
    list_display = (
        'id',
        'phase_days',
        'days_before_call_email',
        'days_to_phone_call',
        'days_after_call_email',
        'days_to_rediffuse',
        'days_to_lock_project',
        'times_to_unlock_project',
        'days_for_admin_management',
        'email_sending_hour',
    )
    search_fields = ('id',)
    list_filter = ('phase_days',) 


admin.site.register(SelectionSettings, SelectionSettingsAdmin)
