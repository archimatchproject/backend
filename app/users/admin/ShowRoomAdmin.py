"""
Module: app.admin

Class: ShowRoomAdmin

Description:
    ShowRoom configuration for the ShowRoom model. Registers the ShowRoom model with the Django
    ShowRoom interface.
"""

from django.contrib import admin

from app.users.models import ShowRoom


class ShowRoomAdmin(admin.ModelAdmin):
    """
    ShowRoom configuration for the Admin model.
    """

    model = ShowRoom


admin.site.register(ShowRoom, ShowRoomAdmin)