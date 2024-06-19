from django.contrib import admin

from app.announcement.models.AnnouncementWorkType import AnnouncementWorkType


class AnnouncementWorkTypeAdmin(admin.ModelAdmin):
    """
    Admin options for AnnouncementWorkType model.

    This class provides customizations for the admin interface of
    the AnnouncementWorkType model in the Django admin site.

    Attributes:
        list_display (tuple): Specifies the fields to display in the list view of the admin interface.
        search_fields (tuple): Specifies the fields that can be searched in the admin interface.

    Methods:
        None
    """

    list_display = ("id", "header", "description")
    search_fields = ("header",)


# Register the admin class with the AnnouncementWorkType model
admin.site.register(AnnouncementWorkType, AnnouncementWorkTypeAdmin)
