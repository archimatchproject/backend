"""
Admin registration module for the ProjectReport model.
"""

from django.contrib import admin

from app.moderation.models.ProjectReport import ProjectReport


class ProjectReportAdmin(admin.ModelAdmin):
    """
    Admin interface for ProjectReport.
    """

    list_display = ("reported_project", "reporting_architect", "status", "decision")
    search_fields = ("reporting_architect__user__email",)


admin.site.register(ProjectReport, ProjectReportAdmin)
