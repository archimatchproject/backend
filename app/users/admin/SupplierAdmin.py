"""
Module: app.admin

Classes:
- SupplierAdmin: Admin configuration for the Supplier model.

Description:
This module registers the Supplier model with the Django admin interface
and specifies basic configurations for managing Supplier instances.

Attributes:
- No module-level attributes defined.

Functions:
- No module-level functions defined.
"""

from django.contrib import admin

from app.users.models import Supplier


class SupplierAdmin(admin.ModelAdmin):
    """
    Admin configuration for the Supplier model.

    Attributes:
    - model: Specifies the Supplier model.

    Methods:
    - No additional methods are defined in this class.
    """

    model = Supplier


admin.site.register(Supplier, SupplierAdmin)
