from django.contrib import admin

from app.users.models import Admin


class AdminAdmin(admin.ModelAdmin):
    model = Admin


admin.site.register(Admin, AdminAdmin)
