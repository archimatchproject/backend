"""
Admin registration module for the Payment model.
"""

from django.contrib import admin

from app.subscription.models.Payment import Payment


class PaymentAdmin(admin.ModelAdmin):
    """
    Admin interface for Payment.
    """

    list_display = (
        "architect",
        "admin_responsable",
        "payment_method",
        "status",
        "subscription_plan",
    )
    search_fields = ("architect__user__email", "subscription_plan__plan_name")


admin.site.register(Payment, PaymentAdmin)
