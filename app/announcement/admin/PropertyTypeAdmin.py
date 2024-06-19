from django.contrib import admin

from app.announcement.models.PropertyType import PropertyType


class PropertyTypeAdmin(admin.ModelAdmin):
    """
    Admin options for PropertyType model.

    This class provides customizations for the admin interface of
    the PropertyType model in the Django admin site.

    Attributes:
        list_display (tuple): Specifies the fields to display in the list view of the admin interface.
        search_fields (tuple): Specifies the fields to enable search functionality in the admin interface.
        list_filter (tuple): Specifies the fields to enable filtering functionality in the admin interface.

    Methods:
        None
    """

    list_display = ("id", "label", "icon", "project_category")
    search_fields = ("label",)
    list_filter = ("project_category",)


# Register the admin class with the PropertyType model
admin.site.register(PropertyType, PropertyTypeAdmin)
