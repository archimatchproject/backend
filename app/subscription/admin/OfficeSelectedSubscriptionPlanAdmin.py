"""
Admin interface for managing OfficeSelectedSubscriptionPlan instances.
This admin interface allows for the management of OfficeSelectedSubscriptionPlan
objects within the Django admin panel. It provides functionalities such as
displaying a list of subscription plans with specific fields, searching by plan
name, and filtering by active status and free plan status.
Attributes:
    list_display (tuple): Fields to display in the list view of the admin panel.
    search_fields (tuple): Fields to include in the search functionality.
    list_filter (tuple): Fields to include in the filter functionality.
Classes:
    OfficeSelectedSubscriptionPlanAdmin: Custom admin interface for OfficeSelectedSubscriptionPlan model.
"""

from django.contrib import admin

from app.subscription.models.OfficeSelectedSubscriptionPlan import OfficeSelectedSubscriptionPlan


class OfficeSelectedSubscriptionPlanAdmin(admin.ModelAdmin):
    """
    Admin interface for OfficeSelectedSubscriptionPlan.
    """

    list_display = (
        "plan_name",
        "plan_price",
        "active",
        "free_plan",
        "start_date",
        "end_date",
        "discount",
        "discount_percentage",
        "announces_number",
        "architects_number_per_announce",
    )
    search_fields = ("plan_name",)
    list_filter = ("active", "free_plan")


admin.site.register(OfficeSelectedSubscriptionPlan, OfficeSelectedSubscriptionPlanAdmin)
