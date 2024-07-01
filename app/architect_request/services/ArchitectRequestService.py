"""
Module containing the service for handling ArchitectRequest logic.

This module defines the service for handling the business logic and exceptions
related to ArchitectRequest creation and management.

Classes:
    ArchitectRequestService: Service class for ArchitectRequest operations.
"""

from django.db import transaction

from rest_framework import status
from rest_framework.response import Response

from app.architect_request.models.ArchitectRequest import ArchitectRequest
from app.architect_request.serializers.ArchitectRequestSerializer import (
    ArchitectRequestInputSerializer,
)
from app.architect_request.serializers.ArchitectRequestSerializer import ArchitectRequestSerializer
from app.core.models.ArchitectSpeciality import ArchitectSpeciality


class ArchitectRequestService:
    """
    Service class for ArchitectRequest operations.

    Handles business logic and exception handling for ArchitectRequest creation and management.

    Methods:
        add_architect_request(data): Handles validation and creation of a new ArchitectRequest.
    """

    @classmethod
    def add_architect_request(cls, data):
        """
        Handles validation and creation of a new ArchitectRequest.

        Args:
            data (dict): The validated data for creating an ArchitectRequest.

        Returns:
            Response: The response object containing the result of the operation.
        """
        serializer = ArchitectRequestInputSerializer(data=data)
        if serializer.is_valid():
            try:
                with transaction.atomic():
                    architect_speciality_id = data["architect_speciality"]
                    architect_speciality = ArchitectSpeciality.objects.get(
                        pk=architect_speciality_id
                    )

                    architect_request = ArchitectRequest(
                        first_name=data["first_name"],
                        last_name=data["last_name"],
                        phone_number=data["phone_number"],
                        address=data["address"],
                        architect_identifier=data["architect_identifier"],
                        email=data["email"],
                        date=data["date"],
                        time_slot=data["time_slot"],
                        architect_speciality=architect_speciality,
                    )
                    # Call the clean method to ensure validation
                    architect_request.clean()
                    architect_request.save()

                    return Response(
                        ArchitectRequestSerializer(architect_request).data,
                        status=status.HTTP_201_CREATED,
                    )
            except ArchitectSpeciality.DoesNotExist:
                return Response(
                    {
                        "error": (
                            f"ArchitectSpeciality with id {architect_speciality_id} does not exist."
                        )
                    },
                    status=status.HTTP_400_BAD_REQUEST,
                )
            except Exception:
                return Response(
                    {"error handling request"},
                    status=status.HTTP_400_BAD_REQUEST,
                )
        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST,
        )
