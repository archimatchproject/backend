from django.contrib import admin

from app.subscription.models.OfficePayment import OfficePayment


class OfficePaymentAdmin(admin.ModelAdmin):
    """
    Admin interface for OfficePayment.
    """
    list_display = (
        "office",
        "admin_responsable",
        "payment_method",
        "status",
        "subscription_plan",
    )
    search_fields = ("office__user__email", "subscription_plan__plan_name")


admin.site.register(OfficePayment, OfficePaymentAdmin)
