from django.contrib import admin

from app.users.models import Supplier


class SupplierAdmin(admin.ModelAdmin):
    model = Supplier


admin.site.register(Supplier, SupplierAdmin)
