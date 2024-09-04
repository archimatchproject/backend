"""
Service module for the SubscriptionPlan model.

This module defines the service for handling the business logic and exceptions
related to SubscriptionPlan creation and management.

Classes:
    TokenPackService: Service class for TokenPack operations.
"""

from django.http import HttpResponse

from rest_framework import status
from rest_framework.exceptions import APIException
from rest_framework.exceptions import NotFound
from rest_framework.response import Response

from app.email_templates.utils import render_to_pdf
from app.subscription.models.ArchitectInvoice import ArchitectInvoice
from app.subscription.models.SupplierInvoice import SupplierInvoice
from app.subscription.serializers.InvoiceSerializer import ArchitectInvoiceSerializer, SupplierInvoiceSerializer
from app.users.models.Architect import Architect
from app.users.models.Supplier import Supplier
from project_core.django import base as settings


class InvoiceService:
    """
    Service class for handling TokenPack operations.

    Handles business logic and exception handling for TokenPack creation and management.
    """

    @classmethod
    def export_invoice(cls, request, id):
        """
        Export invoices to pdf format.
        """
        invoice = ArchitectInvoice.objects.get(pk=id)
        context = {
            "archimatch_img": settings.GLOBAL_PATH + "/architect_logo.png",
            "architect_first_name": invoice.architect.user.first_name,
            "architect_last_name": invoice.architect.user.last_name,
            "architect_phone_number": invoice.architect.user.phone_number,
            "architect_email": invoice.architect.user.email,
            "company_name": invoice.architect.company_name,
            "billing_address": invoice.architect.address,
            "invoice_number": invoice.invoice_number,
            "issue_date": invoice.date.strftime("%d/%m/%Y") if invoice.date else "",
            "plan_name": invoice.plan_name,
            "plan_price": invoice.plan_price,
            "discount": invoice.discount,
            "discount_percentage": invoice.discount_percentage,
            "amount": invoice.amount,
        }
        template_name = "invoice.html"
        pdf = render_to_pdf(template_name, context)
        if pdf:
            response = HttpResponse(pdf, content_type="application/pdf")
            response["Content-Disposition"] = f'attachment; filename="invoice_{id}.pdf"'
            return response
        return HttpResponse("file or pdf not found!")

    @classmethod
    def architect_get_invoices(cls, request):
        """
        Retrieves architect invoices.

        Args:
            request (Request): Django request object containing user ID.

        Returns:
            Response: Response object containing architect data.

        Raises:
            APIException: If there are errors during the process.
        """
        user_id = request.user.id
        try:
            architect = Architect.objects.get(user__id=user_id)
            invoices = ArchitectInvoice.objects.filter(architect=architect)

            invoices_seriliazer = ArchitectInvoiceSerializer(invoices, many=True)
            return Response(
                invoices_seriliazer.data,
                status=status.HTTP_200_OK,
            )
        except Architect.DoesNotExist:
            raise NotFound(detail="Architect not found.", code=status.HTTP_404_NOT_FOUND)
        except APIException as e:
            raise e
        except Exception as e:
            raise APIException(detail=str(e))

    
    @classmethod
    def export_supplier_invoice(cls, request, id):
        """
        Export invoices to pdf format.
        """
        invoice = SupplierInvoice.objects.get(pk=id)
        context = {
            "archimatch_img": settings.GLOBAL_PATH + "/architect_logo.png",
            "supplier_first_name": invoice.supplier.user.first_name,
            "supplier_last_name": invoice.supplier.user.last_name,
            "supplier_phone_number": invoice.supplier.user.phone_number,
            "supplier_email": invoice.supplier.user.email,
            "company_name": invoice.supplier.company_name,
            "billing_address": invoice.supplier.address,
            "invoice_number": invoice.invoice_number,
            "issue_date": invoice.date.strftime("%d/%m/%Y") if invoice.date else "",
            "plan_name": invoice.plan_name,
            "plan_price": invoice.plan_price,
            "discount": invoice.discount,
            "discount_percentage": invoice.discount_percentage,
            "amount": invoice.amount,
        }
        template_name = "invoice.html"
        pdf = render_to_pdf(template_name, context)
        if pdf:
            response = HttpResponse(pdf, content_type="application/pdf")
            response["Content-Disposition"] = f'attachment; filename="invoice_{id}.pdf"'
            return response
        return HttpResponse("file or pdf not found!")

    @classmethod
    def supplier_get_invoices(cls, request):
        """
        Retrieves architect invoices.

        Args:
            request (Request): Django request object containing user ID.

        Returns:
            Response: Response object containing architect data.

        Raises:
            APIException: If there are errors during the process.
        """
        user_id = request.user.id
        try:
            supplier = Supplier.objects.get(user__id=user_id)
            invoices = SupplierInvoice.objects.filter(supplier=supplier)

            invoices_seriliazer = SupplierInvoiceSerializer(invoices, many=True)
            return Response(
                invoices_seriliazer.data,
                status=status.HTTP_200_OK,
            )
        except Architect.DoesNotExist:
            raise NotFound(detail="Architect not found.", code=status.HTTP_404_NOT_FOUND)
        except APIException as e:
            raise e
        except Exception as e:
            raise APIException(detail=str(e))
