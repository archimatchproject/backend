from django import forms
from django.contrib import admin
from django.db import models
from django.forms import SelectMultiple

from app.users.models import Architect, ArchitectType


class ArchitectForm(forms.ModelForm):
    class Meta:
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
    model = Architect
    form = ArchitectForm


admin.site.register(Architect, ArchitectAdmin)


class ArchitectTypeAdmin(admin.ModelAdmin):
    model = ArchitectType


admin.site.register(ArchitectType, ArchitectTypeAdmin)
