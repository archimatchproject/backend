"""
Module: app.admin

Class: MeetingAdmin

Description:
    Meeting configuration for the Meeting model. Registers the Meeting model with the Django
    Meeting interface.
"""

from django.contrib import admin

from app.users.models import Meeting


class MeetingAdmin(admin.ModelAdmin):
    """
    Meeting configuration for the Admin model.
    """

    model = Meeting


admin.site.register(Meeting, MeetingAdmin)