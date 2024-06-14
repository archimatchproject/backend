from app.users.models import Admin
from django.contrib import admin


class AdminAdmin(admin.ModelAdmin):
    model = Admin


admin.site.register(Admin, AdminAdmin)
