from django.contrib import admin

from app.announcement.models.PieceRenovate import PieceRenovate


class PieceRenovateAdmin(admin.ModelAdmin):
    list_display = ("id", "label", "icon", "number")
    search_fields = ("label",)


admin.site.register(PieceRenovate, PieceRenovateAdmin)
