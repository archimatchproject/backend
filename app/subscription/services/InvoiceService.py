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
from app.subscription.models.Invoice import Invoice
from app.subscription.serializers.InvoiceSerializer import InvoiceSerializer
from app.users.models.Architect import Architect
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
        invoice = Invoice.objects.get(pk=id)
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
            return HttpResponse(pdf, content_type="application/pdf")
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
            invoices = Invoice.objects.filter(architect=architect)
            invoices_seriliazer = InvoiceSerializer(invoices)
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
