"""
Module: app.admin

Class: AdminAdmin

Description:
    Admin configuration for the Admin model. Registers the Admin model with the Django
    admin interface.
"""

from django.contrib import admin

from app.users.models.TimeSlot import TimeSlot


class TimeSlotAdmin(admin.ModelAdmin):
    """
    Admin configuration for the TimeSlot model.
    """

    model = TimeSlot


admin.site.register(TimeSlot, TimeSlotAdmin)
