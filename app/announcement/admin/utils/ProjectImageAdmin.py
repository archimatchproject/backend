from django.contrib import admin

from app.announcement.models.utils.ProjectImage import ProjectImage


class ProjectImageAdmin(admin.ModelAdmin):
    list_display = ("id", "id", "image")


admin.site.register(ProjectImage, ProjectImageAdmin)
