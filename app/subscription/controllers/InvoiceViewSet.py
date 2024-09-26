"""
ViewSet module for the Invoice model.
"""

from rest_framework import viewsets
from rest_framework.decorators import action

from app.subscription.models.ArchitectInvoice import ArchitectInvoice
from app.subscription.serializers.InvoiceSerializer import ArchitectInvoiceSerializer
from app.subscription.services.InvoiceService import InvoiceService
from app.core.exception_handler import handle_service_exceptions
from app.core.response_builder import build_response
from rest_framework import status

class InvoiceViewSet(viewsets.ModelViewSet):
    """
    ViewSet for the Invoice model.
    """

    queryset = ArchitectInvoice.objects.all()
    serializer_class = ArchitectInvoiceSerializer

    @action(detail=True, methods=["get"], url_path="export-invoice", url_name="export-invoice")
    @handle_service_exceptions
    def export_invoice(self, request, pk=None):
        """
        Custom action to export an invoice as a PDF.

        Args:
            request (Request): The HTTP request object containing user data.
            pk (int): The primary key of the invoice to export.

        Returns:
            Response: The response object containing the exported PDF or an error message.
        """
        return InvoiceService.export_invoice(request, pk)

    @action(detail=True, methods=["get"], url_path="get-invoices", url_name="get-invoices")
    @handle_service_exceptions
    def architect_get_invoices(self, request):
        """
        Custom action to fetch invoices for a specific architect.

        Args:
            request (Request): The HTTP request object containing user data.
            pk (int): The primary key of the architect whose invoices are to be fetched.

        Returns:
            Response: The response object containing the list of invoices or an error message.
        """
        return InvoiceService.architect_get_invoices(request)
        

