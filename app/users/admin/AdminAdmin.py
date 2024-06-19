"""
Module: app.admin

Class: AdminAdmin

Description:
    Admin configuration for the Admin model. Registers the Admin model with the Django admin interface.

Attributes:
    model: Specifies the Admin model to be administered.

Functions:
    - __init__(self, model_admin_site)
        Initializes the AdminAdmin instance.

        Parameters:
            model_admin_site: The admin site instance for which this admin is being registered.

    - No additional methods are defined in this class.
"""
from django.contrib import admin

from app.users.models import Admin


class AdminAdmin(admin.ModelAdmin):
    """
    Admin configuration for the Admin model.
    """

    model = Admin


admin.site.register(Admin, AdminAdmin)
