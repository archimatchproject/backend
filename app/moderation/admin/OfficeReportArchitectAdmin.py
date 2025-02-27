"""
Admin registration module for the OfficeReportArchitect model.
"""

from django.contrib import admin

from app.moderation.models.OfficeReportArchitect import OfficeReportArchitect


class OfficeReportArchitectAdmin(admin.ModelAdmin):
    """
    Admin interface for OfficeReportArchitect.
    """

    list_display = ("reported_architect", "reporting_office", "status", "decision")
    search_fields = ("reported_architect__user__email", "reporting_office__user__email")


admin.site.register(OfficeReportArchitect, OfficeReportArchitectAdmin)
