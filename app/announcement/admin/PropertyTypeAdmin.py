from django.contrib import admin

from app.announcement.models.PropertyType import PropertyType


class PropertyTypeAdmin(admin.ModelAdmin):
    list_display = ("id", "label", "icon", "project_category")
    search_fields = ("label",)
    list_filter = ("project_category",)


admin.site.register(PropertyType, PropertyTypeAdmin)
