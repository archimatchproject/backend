"""
Admin registration module for the Reason model.
"""

from django.contrib import admin

from app.moderation.models.Reason import Reason


class ReasonAdmin(admin.ModelAdmin):
    """
    Admin interface for Reason.
    """

    list_display = ("name", "report_type")
    search_fields = ("name", "report_type")


admin.site.register(Reason, ReasonAdmin)
