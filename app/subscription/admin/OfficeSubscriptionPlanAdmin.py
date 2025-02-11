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
