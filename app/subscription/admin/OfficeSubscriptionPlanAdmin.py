"""
Admin interface for managing OfficeSubscriptionPlan models.
This class customizes the Django admin interface for the OfficeSubscriptionPlan model,
allowing for the display, search, and filtering of subscription plans.
Attributes:
    list_display (tuple): Fields to display in the admin list view.
    search_fields (tuple): Fields to include in the search functionality.
    list_filter (tuple): Fields to include in the filter sidebar.
Methods:
    None

"""

from django.contrib import admin

from app.subscription.models.OfficeSubscriptionPlan import OfficeSubscriptionPlan


class OfficeSubscriptionPlanAdmin(admin.ModelAdmin):
    """
    Admin interface for OfficeSubscriptionPlan.
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


admin.site.register(OfficeSubscriptionPlan, OfficeSubscriptionPlanAdmin)
