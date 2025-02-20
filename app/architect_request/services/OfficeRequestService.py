"""
Module containing the service for handling OfficeRequest logic.

This module defines the service for handling the business logic and exceptions
related to OfficeRequest creation and management.

Classes:
    OfficeRequestService: Service class for OfficeRequest operations.
"""

from datetime import datetime

from django.db import transaction
from django.db.models import Q
from django.utils import timezone
from django.utils.translation import get_language_from_request

from rest_framework import serializers
from rest_framework import status
from rest_framework.response import Response

from app.announcement import ACCEPTED
from app.announcement import REFUSED
from app.architect_request import AWAITING_DECISION
from app.architect_request import AWAITING_DEMO
from app.architect_request.filters.OfficeRequestFilter import OfficeRequestFilter
from app.architect_request.models.OfficeRequest import OfficeRequest
from app.architect_request.serializers.OfficeRequestRescheduleSerializer import OfficeRequestRescheduleSerializer
from app.architect_request.serializers.OfficeRequestSerializer import OfficeRequestInputSerializer
from app.architect_request.serializers.OfficeRequestSerializer import OfficeRequestSerializer
from app.core.models.Note import Note
from app.core.pagination import CustomPagination
from app.core.serializers.NoteSerializer import NoteSerializer
from app.email_templates.signals import api_success_signal
from app.users.models.Admin import Admin
from app.users.models.ArchimatchUser import ArchimatchUser
from app.users.models.Office import Office
from app.users.serializers.OfficeSerializer import OfficeSerializer
from app.users.utils import generate_password_reset_token
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

            return True, OfficeRequestSerializer(office_request).data

    @classmethod
    def office_request_paginated(cls, request):
        """
        Handle GET request and return paginated OfficeRequest objects filtered by status.

        This method retrieves OfficeRequest objects based on the provided 'account_exists'
        parameter. If 'account_exists' is set to 'accepted', it filters by 'Accepted' status;
        otherwise, it filters by 'Awaiting Demo' and 'Awaiting Decision'. Pagination is applied.

        Args:
            request (HttpRequest): The incoming HTTP request.

        Returns:
            Response: A paginated response containing OfficeRequest objects or an error message.
        """
        cls.update_request_statuses()
        # Check if 'account_exists' is provided and equals 'accepted'
        account_exists = request.GET.get("account_exists")

        if account_exists == "true":
            queryset = OfficeRequest.objects.filter(status="Accepted").order_by("date", "time_slot")
        else:
            queryset = OfficeRequest.objects.filter(status__in=[AWAITING_DEMO, AWAITING_DECISION]).order_by(
                "date", "time_slot"
            )

        filtered_queryset = OfficeRequestFilter(request.GET, queryset=queryset).qs

        paginator = cls.pagination_class()

        page = paginator.paginate_queryset(filtered_queryset, request)
        if page is not None:
            serializer = OfficeRequestSerializer(page, many=True)
            return paginator.get_paginated_response(serializer.data)

        return Response([], status=status.HTTP_400_BAD_REQUEST)

    @classmethod
    def update_request_statuses(cls):
        """
        Update the status of ArchitectRequest instances based on the current date and time.
        Requests that have a meeting date and time that has passed will be updated to
        'Awaiting Decision'.
        """
        now = timezone.now()

        # Filter requests that are still in 'Awaiting Demo' or 'Awaiting Decision' status
        requests_to_update = OfficeRequest.objects.filter(
            Q(date__lt=now.date()) | (Q(date=now.date()) & Q(time_slot__lt=now.time()))
        )

        # Update the status of the filtered requests
        requests_to_update.update(status=AWAITING_DECISION)

        return requests_to_update.count()  # Return the number of updated requests

    @classmethod
    def admin_refuse_office_request(cls, pk):
        """
        Handles refusing an OfficeRequest.

        Args:
            pk (str): The primary key of the OfficeRequest to be refused.

        Returns:
            Response: The response object containing the result of the operation.
        """

        office_request = OfficeRequest.objects.get(pk=pk)
        office_request.status = REFUSED
        office_request.save()
        email_images = settings.REFUSE_ARCHITECT_REQUEST_IMAGES
        signal_data = {
            "template_name": "refuse_architect_request.html",
            "context": {
                "first_name": office_request.office_name,
                "last_name": office_request.office_name,
                "email": office_request.email,
            },
            "to_email": office_request.email,
            "subject": "Refusing Office Request",
            "images": email_images,
        }
        api_success_signal.send(sender=cls, data=signal_data)

        return True, OfficeRequestSerializer(office_request).data

    @classmethod
    def admin_accept_office_request(cls, office_request_id, request):
        """
        Handles accepting an OfficeRequest and creating a new Office.

        Args:
            office_request_id (int): The ID of the OfficeRequest to be accepted.
            request (HttpRequest): The incoming HTTP request.

        Returns:
            Response: The response object containing the result of the operation.
        """
        office_request = OfficeRequest.objects.get(pk=office_request_id)

        meeting_naive_datetime = datetime.combine(office_request.date, office_request.time_slot)
        meeting_aware_datetime = timezone.make_aware(meeting_naive_datetime, timezone.get_current_timezone())

        if timezone.now() < meeting_aware_datetime:
            raise serializers.ValidationError("You cannot accept this request before the scheduled date and time.")

        user_data = {
            "email": office_request.email,
            "username": office_request.email,
            "phone_number": office_request.phone_number,
            "first_name": office_request.office_name,
            "last_name": office_request.office_name,
            "user_type": "Office",
        }

        with transaction.atomic():
            if ArchimatchUser.objects.filter(email=office_request.email).exists():
                raise serializers.ValidationError("An account with this email already exists.")

            user = ArchimatchUser.objects.create(**user_data)
            user.save()

            office = Office.objects.create(
                user=user,
                office_name=office_request.office_name,
                office_address=office_request.office_address,
            )

            office_request.status = ACCEPTED
            office_request.save()

            email_images = settings.ACCEPT_ARCHITECT_REQUEST_IMAGES
            language_code = get_language_from_request(request)
            token = generate_password_reset_token(user.id)
            url = f"""{settings.BASE_FRONTEND_URL}/{language_code}"""
            reset_link = f"{url}/office/login/first-login-password/{token}"
            signal_data = {
                "template_name": "accept_architect_request.html",
                "context": {
                    "first_name": user_data.get("first_name"),
                    "last_name": user_data.get("last_name"),
                    "email": user_data.get("email"),
                    "reset_link": reset_link,
                },
                "to_email": user_data.get("email"),
                "subject": "Acceptance of Office Request",
                "images": email_images,
            }
            api_success_signal.send(sender=cls, data=signal_data)

            return True, OfficeSerializer(office).data

    @classmethod
    def add_note_to_office_request(cls, office_request_id, data):
        """
        Handles adding a note to an OfficeRequest.

        Args:
            office_request_id (int): The ID of the OfficeRequest to which
            the note will be added.
            data (dict): The validated data for creating a new Note.

        Returns:
            Response: The response object containing the result of the operation.
        """

        office_request = OfficeRequest.objects.get(pk=office_request_id)

        serializer = NoteSerializer(data=data)
        serializer.is_valid(raise_exception=True)

        note = Note.objects.create(
            message=serializer.validated_data["message"],
            content_object=office_request,
        )

        return True, NoteSerializer(note).data

    @classmethod
    def reschedule_office_request(cls, office_request_id, data):
        """
        Handles rescheduling an OfficeRequest.

        Args:
            office_request_id (int): The ID of the OfficeRequest to be rescheduled.
            data (dict): The validated data for rescheduling the OfficeRequest.

        Returns:
            Response: The response object containing the result of the operation.
        """

        serializer = OfficeRequestRescheduleSerializer(data=data)
        serializer.is_valid(raise_exception=True)

        office_request = OfficeRequest.objects.get(pk=office_request_id)
        with transaction.atomic():
            office_request.date = serializer.validated_data.get("date")
            office_request.time_slot = serializer.validated_data.get("time_slot")
            office_request.clean()
            office_request.save()

            email_images = settings.REFUSE_ARCHITECT_REQUEST_IMAGES
            signal_data = {
                "template_name": "reschedule_office_request.html",
                "context": {
                    "first_name": office_request.office_name,
                    "last_name": office_request.office_name,
                    "email": office_request.email,
                    "date": office_request.date,
                    "time_slot": office_request.time_slot,
                },
                "to_email": office_request.email,
                "subject": "Rescheduling Office Request",
                "images": email_images,
            }
            api_success_signal.send(sender=cls, data=signal_data)
            return True, OfficeRequestSerializer(office_request).data

    @classmethod
    def admin_assign_office_responsable(cls, pk, admin_id):
        """
        Handles assigning a responsible admin for an OfficeRequest.

        Args:
            pk (str): The primary key of the OfficeRequest to be updated.
            admin_id (str): The primary key of the Admin to be assigned.

        Returns:
            Response: The response object containing the result of the operation.
        """

        office_request = OfficeRequest.objects.get(pk=pk)
        admin = Admin.objects.get(pk=admin_id)
        office_request.meeting_responsable = admin
        office_request.save()

        return (
            True,
            OfficeRequestSerializer(office_request).data,
        )
