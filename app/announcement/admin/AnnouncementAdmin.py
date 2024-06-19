from django.contrib import admin

from app.announcement.models import Announcement


class AnnouncementAdmin(admin.ModelAdmin):
    model = Announcement


admin.site.register(Announcement, AnnouncementAdmin)
