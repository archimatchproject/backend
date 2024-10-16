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
from app.users.models.SupplierCoverImage import SupplierCoverImage


class SupplierCoverImageInline(admin.TabularInline):
    """
    Inline admin configuration for SupplierCoverImage model.

    This inline admin class allows managing SupplierCoverImage instances within the SupplierAdmin.
    """

    model = SupplierCoverImage
    extra = 3
    max_num = 3


class SupplierAdmin(admin.ModelAdmin):
    """
    Admin configuration for the Supplier model.

    Attributes:
    - model: Specifies the Supplier model.
    """

    model = Supplier
    inlines = [SupplierCoverImageInline]


admin.site.register(Supplier, SupplierAdmin)
