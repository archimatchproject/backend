"""
Exposed URLs for the Invoice model.

This module defines the URL patterns for the InvoiceViewSet,
providing separate paths for each CRUD operation.
"""

from django.urls import path

from app.subscription.controllers.InvoiceViewSet import InvoiceViewSet


invoice_urlpatterns = [
    path(
        "export-invoice/<int:pk>/",
        InvoiceViewSet.as_view({"get": "export_invoice"}),
        name="export-invoice",
    ),
    path(
        "get-invoices/",
        InvoiceViewSet.as_view({"get": "architect_get_invoices"}),
        name="get-invoices",
    ),
]
