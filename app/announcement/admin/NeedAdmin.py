from django.contrib import admin

from app.announcement.models.Need import Need


class NeedAdmin(admin.ModelAdmin):
    list_display = ("id", "label", "icon", "architect_speciality")
    search_fields = ("label",)
    list_filter = ("architect_speciality",)


admin.site.register(Need, NeedAdmin)
