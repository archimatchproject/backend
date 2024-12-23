"""
Admin registration module for the SelectionReport model.
"""

from django.contrib import admin
from app.moderation.models.SelectionReport import SelectionReport


class SelectionReportAdmin(admin.ModelAdmin):
    """
    Admin interface for SelectionReport.
    """

    list_display = ("selection", "reporting_client", "status", "created_at")
    search_fields = ("selection__name", "reporting_client__user__first_name", "status")
    list_filter = ("status", "created_at")

    def __str__(self):
        """
        Returns a string representation of the SelectionReportAdmin instance.
        """
        return f"SelectionReportAdmin for {self.selection.name} - {self.status}"


admin.site.register(SelectionReport, SelectionReportAdmin)
