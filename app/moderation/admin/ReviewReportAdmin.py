"""
Admin registration module for the ReviewReport model.
"""

from django.contrib import admin

from app.moderation.models.ReviewReport import ReviewReport


class ReviewReportAdmin(admin.ModelAdmin):
    """
    Admin interface for ReviewReport.
    """

    list_display = ("reported_review", "reporting_architect", "status", "decision")
    search_fields = ("reported_review__comment", "reporting_architect__user__email")


admin.site.register(ReviewReport, ReviewReportAdmin)
