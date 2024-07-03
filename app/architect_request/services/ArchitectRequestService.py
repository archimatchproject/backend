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
from app.architect_request.serializers.ArchitectRequestSerializer import ArchitectAcceptSerializer
from app.architect_request.serializers.ArchitectRequestSerializer import (
    ArchitectRequestInputSerializer,
)
from app.architect_request.serializers.ArchitectRequestSerializer import ArchitectRequestSerializer
from app.core.models.ArchitectSpeciality import ArchitectSpeciality
from app.users.models.Admin import Admin
from app.users.models.ArchimatchUser import ArchimatchUser
from app.users.models.Architect import Architect
from app.users.serializers.ArchitectSerializer import ArchitectSerializer


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
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @classmethod
    def admin_accept_architect_request(cls, architect_request_id, data):
        """
        Handles accepting an ArchitectRequest and creating a new Architect.

        Args:
            architect_request_id (int): The ID of the ArchitectRequest to be accepted.
            data (dict): The validated data for creating a new Architect.

        Returns:
            Response: The response object containing the result of the operation.
        """
        try:
            architect_request = ArchitectRequest.objects.get(pk=architect_request_id)
        except ArchitectRequest.DoesNotExist:
            return Response(
                {"error": "ArchitectRequest not found."},
                status=status.HTTP_404_NOT_FOUND,
            )

        # Validate the incoming data using the serializer
        serializer = ArchitectAcceptSerializer(data=data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        validated_data = serializer.validated_data

        user_data = {
            "email": architect_request.email,
            "username": architect_request.email,
            "phone_number": architect_request.phone_number,
            "first_name": architect_request.first_name,
            "last_name": architect_request.last_name,
        }

        try:
            with transaction.atomic():
                user = ArchimatchUser.objects.create(**user_data)
                user.save()

                architect = Architect.objects.create(
                    user=user,
                    address=architect_request.address,
                    architect_identifier=architect_request.architect_identifier,
                    architect_speciality=architect_request.architect_speciality,
                )

                # Assign preferences
                for field in [
                    "project_categories",
                    "property_types",
                    "work_types",
                    "architectural_styles",
                ]:
                    items = validated_data.get(field, [])
                    if items:
                        getattr(architect, field).set(items)

                architect_request.status = "Accepted"
                architect_request.save()

                return Response(
                    ArchitectSerializer(architect).data,
                    status=status.HTTP_201_CREATED,
                )
        except Exception as e:
            return Response(
                {"error": str(e)},
                status=status.HTTP_400_BAD_REQUEST,
            )

    @classmethod
    def admin_refuse_architect_request(cls, pk):
        """
        Handles refusing an ArchitectRequest.

        Args:
            pk (str): The primary key of the ArchitectRequest to be refused.

        Returns:
            Response: The response object containing the result of the operation.
        """
        try:
            architect_request = ArchitectRequest.objects.get(pk=pk)
            architect_request.status = "Refused"
            architect_request.save()

            return Response(
                ArchitectRequestSerializer(architect_request).data,
                status=status.HTTP_200_OK,
            )
        except ArchitectRequest.DoesNotExist:
            return Response(
                {"error": "ArchitectRequest not found."},
                status=status.HTTP_404_NOT_FOUND,
            )

    @classmethod
    def admin_assign_responsable(cls, pk, admin_id):
        """
        Handles assigning a responsable admin for an ArchitectRequest.

        Args:
            pk (str): The primary key of the ArchitectRequest to be updated.
            admin_id (str): The primary key of the Admin to be assigned.

        Returns:
            Response: The response object containing the result of the operation.
        """
        try:
            architect_request = ArchitectRequest.objects.get(pk=pk)
            admin = Admin.objects.get(pk=admin_id)
            architect_request.meeting_responsable = admin
            architect_request.save()

            return Response(
                ArchitectRequestSerializer(architect_request).data,
                status=status.HTTP_200_OK,
            )
        except ArchitectRequest.DoesNotExist:
            return Response(
                {"error": "ArchitectRequest not found."},
                status=status.HTTP_404_NOT_FOUND,
            )
        except Admin.DoesNotExist:
            return Response(
                {"error": "Admin not found."},
                status=status.HTTP_404_NOT_FOUND,
            )
