"""
Admin registration module for the SelectedSubscriptionPlan model.
"""

from django.contrib import admin

from app.subscription.models.SelectedSubscriptionPlan import SelectedSubscriptionPlan


class PlanServiceInline(admin.TabularInline):
    """
    Inline admin interface for PlanService.
    """

    model = SelectedSubscriptionPlan.services.through
    extra = 1


class SelectedSubscriptionPlanAdmin(admin.ModelAdmin):
    """
    Admin interface for SelectedSubscriptionPlan.
    """

    inlines = [PlanServiceInline]

    list_display = (
        "plan_name",
        "plan_price",
        "remaining_tokens",
        "active",
        "free_plan",
        "start_date",
        "end_date",
    )
    search_fields = ("plan_name",)
    list_filter = ("active", "free_plan")


admin.site.register(SelectedSubscriptionPlan, SelectedSubscriptionPlanAdmin)
