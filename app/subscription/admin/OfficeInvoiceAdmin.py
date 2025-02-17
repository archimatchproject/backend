"""
This class customizes the Django admin interface for the OfficeInvoice model by specifying
the fields to display in the list view, the fields to include in the search functionality,
and the fields to include in the filter functionality.

"""

from django.contrib import admin

from app.subscription.models.OfficeInvoice import OfficeInvoice


@admin.register(OfficeInvoice)
class OfficeInvoiceAdmin(admin.ModelAdmin):
    """
    Admin class for customizing the Invoice model's admin interface for OfficeInvoices.

    Attributes:
        list_display (tuple): Specifies the fields to display in the list view.
        search_fields (tuple): Specifies the fields to include in the search functionality.
        list_filter (tuple): Specifies the fields to include in the filter functionality.
    """

    list_display = (
        "office",
        "amount",
        "date",
    )
    search_fields = ("office__user__email",)
    list_filter = ("date",)
