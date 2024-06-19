"""
Module: app.admin

Classes:
- ClientAdmin: Admin configuration for the Client model.

Description:
This module registers the Client model with the Django admin interface
and defines custom configurations for managing Client instances.

"""

from django.contrib import admin

from app.users.models import Client


class ClientAdmin(admin.ModelAdmin):
    """
    Admin configuration for the Client model.

    Attributes:
    - model: Specifies the Client model.
    - list_display: Specifies the fields to display in the list view of Client instances.

    """

    model = Client
    list_display = ["id", "user"]


admin.site.register(Client, ClientAdmin)
