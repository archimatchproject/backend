from django.contrib import admin

from app.announcement.models.ProjectCategory import ProjectCategory


class ProjectCategoryAdmin(admin.ModelAdmin):
    list_display = ("id", "label", "icon")
    search_fields = ("label",)


admin.site.register(ProjectCategory, ProjectCategoryAdmin)
