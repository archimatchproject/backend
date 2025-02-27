"""
Admin registration module for the Decision model.
"""

from django.contrib import admin

from app.moderation.models.Decision import Decision


class DecisionAdmin(admin.ModelAdmin):
    """
    Admin interface for the Decision model.
    """

    list_display = ("name", "report_type")
    search_fields = ("name", "report_type")


admin.site.register(Decision, DecisionAdmin)
