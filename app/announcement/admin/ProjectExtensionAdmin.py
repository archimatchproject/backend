from django.contrib import admin

from app.announcement.models.ProjectExtension import ProjectExtension


class ProjectExtensionAdmin(admin.ModelAdmin):
    """
    Admin options for ProjectExtension model.

    This class provides customizations for the admin interface of
    the ProjectExtension model in the Django admin site.

    Attributes:
        list_display (tuple): Specifies the fields to display in the list view of the admin interface.
        search_fields (tuple): Specifies the fields that can be searched in the admin interface.

    Methods:
        None
    """

    list_display = ("id", "label", "icon")
    search_fields = ("label",)


# Register the admin class with the ProjectExtension model
admin.site.register(ProjectExtension, ProjectExtensionAdmin)
