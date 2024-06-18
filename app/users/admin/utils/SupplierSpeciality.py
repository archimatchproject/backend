from app.users.models.utils.SupplierSpeciality import SupplierSpeciality
from django.contrib import admin


class SupplierSpecialityAdmin(admin.ModelAdmin):
    model = SupplierSpeciality


admin.site.register(SupplierSpeciality, SupplierSpecialityAdmin)