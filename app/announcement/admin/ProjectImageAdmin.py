from django.contrib import admin

from app.announcement.models.ProjectImage import ProjectImage


class ProjectImageAdmin(admin.ModelAdmin):
    """
    Admin options for ProjectImage model.

    This class provides customizations for the admin interface of
    the ProjectImage model in the Django admin site.

    Attributes:
        list_display (tuple): Specifies the fields to display in the list view of the admin interface.

    Methods:
        None
    """

    list_display = ("id", "image")


# Register the admin class with the ProjectImage model
admin.site.register(ProjectImage, ProjectImageAdmin)
