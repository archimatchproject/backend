from django.contrib import admin
from app.announcement.models.utils.ProjectExtension import ProjectExtension

class ProjectExtensionAdmin(admin.ModelAdmin):
    list_display = ('id','label', 'icon')
    search_fields = ('label',)

admin.site.register(ProjectExtension, ProjectExtensionAdmin)