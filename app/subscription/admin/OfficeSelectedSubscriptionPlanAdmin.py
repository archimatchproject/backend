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
        "architects_number_per_announce"
    )
    search_fields = ("plan_name",)
    list_filter = ("active", "free_plan")


admin.site.register(OfficeSelectedSubscriptionPlan, OfficeSelectedSubscriptionPlanAdmin)
