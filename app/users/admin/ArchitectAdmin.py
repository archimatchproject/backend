"""
Module: app.admin

Classes:
- ArchitectForm: Form class for the Architect model, defining fields and widgets.

- ArchitectAdmin: Admin configuration for the Architect model.

- ArchitectTypeAdmin: Admin configuration for the ArchitectType model.

Description:
This module registers the Architect and ArchitectType models with the Django admin interface
and defines custom forms and configurations for managing these models.

"""

from django import forms
from django.contrib import admin

from app.users.models import Architect, ArchitectType




class ArchitectAdmin(admin.ModelAdmin):
    """
    Admin configuration for the Architect model.

    Attributes:
    - model: Specifies the Architect model.
    - form: Specifies the custom form (ArchitectForm) to use for managing Architect instances.

    """

    model = Architect


admin.site.register(Architect, ArchitectAdmin)

