from django.contrib import admin

from app.announcement.models.Need import Need


class NeedAdmin(admin.ModelAdmin):
    """
    Admin options for Need model.

    This class provides customizations for the admin interface of
    the Need model in the Django admin site.

    Attributes:
        list_display (tuple): Specifies the fields to display in the list view of the admin interface.
        search_fields (tuple): Specifies the fields that can be searched in the admin interface.
        list_filter (tuple): Specifies the fields to use as filters in the admin interface.

    Methods:
        None
    """

    list_display = ("id", "label", "icon", "architect_speciality")
    search_fields = ("label",)
    list_filter = ("architect_speciality",)


# Register the admin class with the Need model
admin.site.register(Need, NeedAdmin)
