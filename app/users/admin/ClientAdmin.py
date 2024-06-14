from app.users.models import Client
from django.contrib import admin


class ClientAdmin(admin.ModelAdmin):
    model = Client
    list_display = ["id", "user"]


admin.site.register(Client, ClientAdmin)
