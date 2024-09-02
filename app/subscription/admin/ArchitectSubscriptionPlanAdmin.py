"""
Admin registration module for the SubscriptionPlan model.
"""

from django.contrib import admin

from app.subscription.models.ArchitectSubscriptionPlan import ArchitectSubscriptionPlan


class PlanServiceInline(admin.TabularInline):
    """
    Inline admin interface for PlanService.
    """

    model = SubscriptionPlan.services.through
    extra = 1


class ArchitectSubscriptionPlanAdmin(admin.ModelAdmin):
    """
    Admin interface for SubscriptionPlan.
    """

    inlines = [PlanServiceInline]

    list_display = (
        "plan_name",
        "plan_price",
        "active",
        "free_plan",
        "discount",
        "discount_percentage",
        "start_date",
        "end_date",
        "discount_message",
    )
    search_fields = ("plan_name",)
    list_filter = ("active", "free_plan")


admin.site.register(ArchitectSubscriptionPlan, ArchitectSubscriptionPlanAdmin)
