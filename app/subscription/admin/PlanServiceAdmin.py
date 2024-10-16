"""
Admin registration module for the PlanService model.
"""

from django.contrib import admin

from app.subscription.models.PlanService import PlanService


class PlanServiceAdmin(admin.ModelAdmin):
    """
    Admin interface for PlanService.
    """

    list_display = ("description",)
    search_fields = ("description",)


admin.site.register(PlanService, PlanServiceAdmin)
