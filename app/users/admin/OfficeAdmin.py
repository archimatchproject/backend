"""
Module: app.admin

Classes:
- OfficeForm: Form class for the Office model, defining fields and widgets.

- OfficeAdmin: Admin configuration for the Office model.


Description:
This module registers the Office and ArchitectType models with the Django admin interface
and defines custom forms and configurations for managing these models.

"""

from django.contrib import admin

from app.users.models import Office


class OfficeAdmin(admin.ModelAdmin):
    """
    Admin configuration for the Office model.

    Attributes:
    - model: Specifies the Office model.
    - form: Specifies the custom form (OfficeForm) to use for managing Office instances.

    """

    model = Office


admin.site.register(Office, OfficeAdmin)
