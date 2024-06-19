from django.contrib import admin

from app.announcement.models.utils.AnnouncementWorkType import AnnouncementWorkType


class AnnouncementWorkTypeAdmin(admin.ModelAdmin):
    list_display = ("id", "header", "description")
    search_fields = ("header",)


admin.site.register(AnnouncementWorkType, AnnouncementWorkTypeAdmin)
