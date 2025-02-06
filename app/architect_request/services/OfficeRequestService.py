"""
Module containing the service for handling OfficeRequest logic.

This module defines the service for handling the business logic and exceptions
related to OfficeRequest creation and management.

Classes:
    OfficeRequestService: Service class for OfficeRequest operations.
"""

from django.db import transaction


from app.architect_request.models.OfficeRequest import OfficeRequest

from app.architect_request.serializers.OfficeRequestSerializer import (
    OfficeRequestInputSerializer,
)
from app.architect_request.serializers.ArchitectRequestSerializer import (
    ArchitectRequestSerializer,
)

from app.core.pagination import CustomPagination

from app.email_templates.signals import api_success_signal

from project_core.django import base as settings


class OfficeRequestService:
    """
    Service class for OfficeRequest operations.

    Handles business logic and exception handling for OfficeRequest creation and management.

    Methods:
        add_office_request(data): Handles validation and creation of a new OfficeRequest.
    """

    pagination_class = CustomPagination

    @classmethod
    def add_office_request(cls, data):
        """
        Handles validation and creation of a new OfficeRequest.

        Args:
            data (dict): The validated data for creating an OfficeRequest.

        Returns:
            Response: The response object containing the result of the operation.
        """
        serializer = OfficeRequestInputSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        with transaction.atomic():

            field_names = [
                "office_name",
                "phone_number",
                "office_address",
                "office_identifier",
                "email",
                "date",
                "time_slot",
                "city",
            ]

            office_request = OfficeRequest()
            for field in field_names:
                setattr(office_request, field, data.get(field))

            office_request.clean()
            office_request.save()
            email_images = settings.ARCHITECT_REQUEST_IMAGES

            signal_data = {
                "template_name": "architect_request.html",
                "context": {
                    "first_name": data.get("office_name"),
                    "last_name": data.get("office_name"),
                    "date": data.get("date"),
                    "time_slot": data.get("time_slot"),
                    "email": data.get("email"),
                },
                "to_email": data.get("email"),
                "subject": "Office Account Creation",
                "images": email_images,
            }
            api_success_signal.send(sender=cls, data=signal_data)

            return True, ArchitectRequestSerializer(office_request).data
