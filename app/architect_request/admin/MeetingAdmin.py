"""
Module: app.admin

Class: MeetingAdmin

Description:
    Admin configuration for the Meeting model. Registers the Meeting model with the Django admin interface.
"""
from django.contrib import admin

from app.architect_request.models import Meeting


class MeetingAdmin(admin.ModelAdmin):

    """
    Admin configuration for the Meeting model.
    """

    model = Meeting


admin.site.register(Meeting, MeetingAdmin)
