"""
Admin registration module for the SubscriptionPlan model.
"""

from django.contrib import admin

from app.subscription.models.SupplierSubscriptionPlan import SupplierSubscriptionPlan





class SupplierSubscriptionPlanAdmin(admin.ModelAdmin):
    """
    Admin interface for SubscriptionPlan.
    """


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


admin.site.register(SupplierSubscriptionPlan, SupplierSubscriptionPlanAdmin)
