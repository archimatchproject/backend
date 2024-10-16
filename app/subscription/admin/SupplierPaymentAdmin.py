"""
Admin registration module for the Payment model.
"""

from django.contrib import admin

from app.subscription.models.SupplierPayment import SupplierPayment


class SupplierPaymentAdmin(admin.ModelAdmin):
    """
    Admin interface for Payment.
    """

    list_display = (
        "supplier",
        "admin_responsable",
        "payment_method",
        "status",
        "subscription_plan",
    )
    search_fields = ("supplier__user__email", "subscription_plan__plan_name")


admin.site.register(SupplierPayment, SupplierPaymentAdmin)
