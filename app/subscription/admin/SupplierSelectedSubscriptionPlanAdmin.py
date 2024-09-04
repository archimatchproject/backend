"""
Admin registration module for the SelectedSubscriptionPlan model.
"""

from django.contrib import admin

from app.subscription.models.SupplierSelectedSubscriptionPlan import SupplierSelectedSubscriptionPlan





class SupplierSelectedSubscriptionPlanAdmin(admin.ModelAdmin):
    """
    Admin interface for SelectedSubscriptionPlan.
    """

    list_display = (
        "plan_name",
        "plan_price",
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


admin.site.register(SupplierSelectedSubscriptionPlan, SupplierSelectedSubscriptionPlanAdmin)
