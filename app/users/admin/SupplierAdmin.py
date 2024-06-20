"""
Module: app.admin

Classes:
- SupplierAdmin: Admin configuration for the Supplier model.

Description:
This module registers the Supplier model with the Django admin interface
and specifies basic configurations for managing Supplier instances.

"""

from django.contrib import admin

from app.users.models import Supplier


class SupplierAdmin(admin.ModelAdmin):
    """
    Admin configuration for the Supplier model.

    Attributes:
    - model: Specifies the Supplier model.
    """

    model = Supplier


admin.site.register(Supplier, SupplierAdmin)
