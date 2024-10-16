"""
Module: app.admin

Class: AdminAdmin

Description:
    Admin configuration for the Admin model. Registers the Admin model with the Django
    admin interface.
"""

from django.contrib import admin

from app.users.models.Unavailability import Unavailability


class UnavailabilityAdmin(admin.ModelAdmin):
    """
    Admin configuration for the Unavailability model.
    """

    model = Unavailability


admin.site.register(Unavailability, UnavailabilityAdmin)
