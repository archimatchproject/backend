"""
Module for configuring the admin interface for the Invoice model.

This module defines the admin class for the Invoice model, customizing the admin
interface to manage Invoice instances effectively.

Classes:
    InvoiceAdmin: Admin class for customizing the Invoice model's admin interface.
"""

from django.contrib import admin

from app.subscription.models.SupplierInvoice import SupplierInvoice




@admin.register(SupplierInvoice)
class SupplierInvoiceAdmin(admin.ModelAdmin):
    """
    Admin class for customizing the Invoice model's admin interface.

    Attributes:
        list_display (tuple): Specifies the fields to display in the list view.
        search_fields (tuple): Specifies the fields to include in the search functionality.
        list_filter (tuple): Specifies the fields to include in the filter functionality.
    """

    list_display = (
        "supplier",
        "amount",
        "date",
    )
    search_fields = ("supplier__user__email",)
    list_filter = ("date",)