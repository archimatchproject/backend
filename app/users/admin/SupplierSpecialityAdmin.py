"""
Module: app.admin

Classes:
- SupplierSpecialityAdmin: Admin configuration for the SupplierSpeciality model.

Description:
This module registers the SupplierSpeciality model with the Django admin interface
and specifies basic configurations for managing SupplierSpeciality instances.

"""
from django.contrib import admin

from app.users.models import SupplierSpeciality


class SupplierSpecialityAdmin(admin.ModelAdmin):
    """
    Admin configuration for the SupplierSpeciality model.

    Attributes:
    - model: Specifies the SupplierSpeciality model.
    """

    model = SupplierSpeciality


admin.site.register(SupplierSpeciality, SupplierSpecialityAdmin)
