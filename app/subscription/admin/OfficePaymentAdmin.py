"""
This module defines the admin interface for the OfficePayment model.
Classes:
    OfficePaymentAdmin: Customizes the admin interface for the OfficePayment model.
Attributes:
    list_display (tuple): Specifies the fields to display in the list view of the admin interface.
    search_fields (tuple): Specifies the fields to include in the search functionality of the admin interface.
"""

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
