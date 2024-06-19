from django.contrib import admin

from app.announcement.models.ProjectImage import ProjectImage


class ProjectImageAdmin(admin.ModelAdmin):
    list_display = ("id", "image")


admin.site.register(ProjectImage, ProjectImageAdmin)
