from django.contrib import admin

from app.users.models import Client


class ClientAdmin(admin.ModelAdmin):
    model = Client
    list_display = ["id", "user"]


admin.site.register(Client, ClientAdmin)
