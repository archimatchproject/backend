from django.contrib import admin

from app.announcement.models import Announcement


class AnnouncementAdmin(admin.ModelAdmin):
    """
    Custom admin options for Announcement model.

    This class provides customizations for the admin interface of
    the Announcement model in the Django admin site.

    Attributes:
        model (type): The Django model class handled by this admin class.

    Methods:
        None
    """

    model = Announcement


# Register the admin class with the Announcement model
admin.site.register(Announcement, AnnouncementAdmin)
