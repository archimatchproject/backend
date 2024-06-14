from app.announcement.models import Announcement
from django.contrib import admin


class AnnouncementAdmin(admin.ModelAdmin):
    model = Announcement
    
admin.site.register(Announcement, AnnouncementAdmin)