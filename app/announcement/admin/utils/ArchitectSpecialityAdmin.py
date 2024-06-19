from django.contrib import admin

from app.announcement.models.utils.ArchitectSpeciality import ArchitectSpeciality


class ArchitectSpecialityAdmin(admin.ModelAdmin):
    list_display = ("id", "label", "icon")
    search_fields = ("label",)


admin.site.register(ArchitectSpeciality, ArchitectSpecialityAdmin)
