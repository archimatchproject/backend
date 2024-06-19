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


class ArchitectForm(forms.ModelForm):
    """
    Form class for the Architect model.

    Fields:
    - Meta: Specifies the model (Architect) and fields to include in the form.
        - model: Specifies the Architect model.
        - fields: Specifies to include all fields of the Architect model.
        - widgets: Specifies custom widgets for multi-select fields.


    """

    class Meta:
        """
        Meta class for ArchitectForm.

        """

        model = Architect
        fields = "__all__"
        widgets = {
            "work_types": forms.SelectMultiple(attrs={"size": 5}),
            "house_types": forms.SelectMultiple(attrs={"size": 5}),
            "services": forms.SelectMultiple(attrs={"size": 5}),
            "locations": forms.SelectMultiple(attrs={"size": 20}),
            "work_surfaces": forms.SelectMultiple(attrs={"size": 5}),
            "budgets": forms.SelectMultiple(attrs={"size": 5}),
        }


class ArchitectAdmin(admin.ModelAdmin):
    """
    Admin configuration for the Architect model.

    Attributes:
    - model: Specifies the Architect model.
    - form: Specifies the custom form (ArchitectForm) to use for managing Architect instances.

    """

    model = Architect
    form = ArchitectForm


admin.site.register(Architect, ArchitectAdmin)


class ArchitectTypeAdmin(admin.ModelAdmin):
    """
    Admin configuration for the ArchitectType model.

    Attributes:
    - model: Specifies the ArchitectType model.

    """

    model = ArchitectType


admin.site.register(ArchitectType, ArchitectTypeAdmin)
