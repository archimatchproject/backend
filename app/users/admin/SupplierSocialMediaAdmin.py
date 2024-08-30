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
from app.users.models.SupplierSocialMedia import SupplierSocialMedia


class SupplierSocialMediaAdmin(admin.ModelAdmin):
    """
    Admin configuration for the Supplier model.

    Attributes:
    - model: Specifies the Supplier model.
    """

    model = SupplierSocialMedia


admin.site.register(Supplier, SupplierSocialMediaAdmin)
