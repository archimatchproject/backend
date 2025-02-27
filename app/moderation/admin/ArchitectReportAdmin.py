"""
Admin registration module for the ArchitectReport model.
"""

from django.contrib import admin

from app.moderation.models.ArchitectReport import ArchitectReport


class ArchitectReportAdmin(admin.ModelAdmin):
    """
    Admin interface for ArchitectReport.
    """

    list_display = ("reported_architect", "reporting_client", "status", "decision")
    search_fields = ("reported_architect__user__email", "reporting_client__user__email")


admin.site.register(ArchitectReport, ArchitectReportAdmin)
