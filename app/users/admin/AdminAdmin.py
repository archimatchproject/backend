"""
Module: app.admin

Class: AdminAdmin

Description:
    Admin configuration for the Admin model. Registers the Admin model with the Django
    admin interface.
"""

from django.contrib import admin

from app.users.models import Admin


class AdminAdmin(admin.ModelAdmin):
    """
    Admin configuration for the Admin model.
    """

    model = Admin


admin.site.register(Admin, AdminAdmin)
