from app.users.models import Supplier
from django.contrib import admin


class SupplierAdmin(admin.ModelAdmin):
    model = Supplier


admin.site.register(Supplier, SupplierAdmin)
