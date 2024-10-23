"""
Admin registration module for the SelectedSubscriptionPlan model.
"""

from django.contrib import admin

from app.subscription.models.ArchitectSelectedSubscriptionPlan import ArchitectSelectedSubscriptionPlan




class ArchitectSelectedSubscriptionPlanAdmin(admin.ModelAdmin):
    """
    Admin interface for SelectedSubscriptionPlan.
    """


    list_display = (
        "plan_name",
        "plan_price",
        "remaining_tokens",
        "active",
        "free_plan",
        "start_date",
        "end_date",
        "number_tokens",
        "discount",
        "discount_percentage",
    )
    search_fields = ("plan_name",)
    list_filter = ("active", "free_plan")


admin.site.register(ArchitectSelectedSubscriptionPlan, ArchitectSelectedSubscriptionPlanAdmin)
