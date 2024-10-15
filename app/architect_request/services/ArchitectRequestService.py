"""
Module containing the service for handling ArchitectRequest logic.

This module defines the service for handling the business logic and exceptions
related to ArchitectRequest creation and management.

Classes:
    ArchitectRequestService: Service class for ArchitectRequest operations.
"""

from django.db import transaction
from django.utils.translation import get_language_from_request

from rest_framework import serializers
from rest_framework import status
from rest_framework.exceptions import APIException
from rest_framework.exceptions import NotFound
from rest_framework.response import Response

from app.announcement.serializers.ArchitecturalStyleSerializer import ArchitecturalStyleSerializer
from app.announcement.serializers.ProjectCategorySerializer import ProjectCategorySerializer
from app.announcement.serializers.PropertyTypeSerializer import PropertyTypeSerializer
from app.announcement.serializers.WorkTypeSerializer import WorkTypeSerializer
from app.architect_request import AWAITING_DECISION, AWAITING_DEMO, TIME_SLOT_CHOICES
from app.architect_request.filters.ArchitectRequestFilter import ArchitectRequestFilter
from app.architect_request.models.ArchitectRequest import ArchitectRequest
from app.architect_request.serializers.ArchitectRequestRescheduleSerializer import (
    ArchitectRequestRescheduleSerializer,
)
from app.architect_request.serializers.ArchitectRequestSerializer import ArchitectAcceptSerializer
from app.architect_request.serializers.ArchitectRequestSerializer import (
    ArchitectRequestInputSerializer,
)
from app.architect_request.serializers.ArchitectRequestSerializer import ArchitectRequestSerializer
from app.core.models.ArchitectSpeciality import ArchitectSpeciality
from app.core.models.ArchitecturalStyle import ArchitecturalStyle
from app.core.models.Note import Note
from app.core.models.ProjectCategory import ProjectCategory
from app.core.models.PropertyType import PropertyType
from app.core.models.WorkType import WorkType
from app.core.pagination import CustomPagination
from app.core.serializers.NoteSerializer import NoteSerializer
from app.email_templates.signals import api_success_signal
from app.users import PROJECT_COMPLEXITY_CHOICES
from app.users import YEARS_EXPERIENCE_CHOICES
from app.users.models.Admin import Admin
from app.users.models.ArchimatchUser import ArchimatchUser
from app.users.models.Architect import Architect
from app.users.serializers.ArchitectSerializer import ArchitectSerializer
from app.users.utils import generate_password_reset_token
from project_core.django import base as settings
from django.utils import timezone
from django.db.models import Q
class ArchitectRequestService:
    """
    Service class for ArchitectRequest operations.

    Handles business logic and exception handling for ArchitectRequest creation and management.

    Methods:
        add_architect_request(data): Handles validation and creation of a new ArchitectRequest.
    """

    pagination_class = CustomPagination

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
        serializer.is_valid(raise_exception=True)
        with transaction.atomic():
            architect_speciality_id = data.get("architect_speciality")
            architect_speciality = ArchitectSpeciality.objects.get(pk=architect_speciality_id)

            field_names = [
                "first_name",
                "last_name",
                "phone_number",
                "address",
                "architect_identifier",
                "email",
                "date",
                "time_slot",
                "city",
            ]

            architect_request = ArchitectRequest()
            for field in field_names:
                setattr(architect_request, field, data.get(field))

            architect_request.architect_speciality = architect_speciality

            architect_request.clean()
            architect_request.save()
            email_images = settings.ARCHITECT_REQUEST_IMAGES

            signal_data = {
                "template_name": "architect_request.html",
                "context": {
                    "first_name": data.get("first_name"),
                    "last_name": data.get("last_name"),
                    "date": data.get("date"),
                    "time_slot": data.get("time_slot"),
                    "email": data.get("email"),
                },
                "to_email": data.get("email"),
                "subject": "Architect Account Creation",
                "images": email_images,
            }
            api_success_signal.send(sender=cls, data=signal_data)

            return True,ArchitectRequestSerializer(architect_request).data


    @classmethod
    def admin_accept_architect_request(cls, architect_request_id, request):
        """
        Handles accepting an ArchitectRequest and creating a new Architect.

        Args:
            architect_request_id (int): The ID of the ArchitectRequest to be accepted.
            data (dict): The validated data for creating a new Architect.

        Returns:
            Response: The response object containing the result of the operation.
        """
        data = request.data
        architect_request = ArchitectRequest.objects.get(pk=architect_request_id)
        
        serializer = ArchitectAcceptSerializer(data=data)

        serializer.is_valid(raise_exception=True)

        validated_data = serializer.validated_data
        user_data = {
            "email": architect_request.email,
            "username": architect_request.email,
            "phone_number": architect_request.phone_number,
            "first_name": architect_request.first_name,
            "last_name": architect_request.last_name,
        }

        with transaction.atomic():
            user = ArchimatchUser.objects.create(**user_data)
            user.save()
            architect = Architect.objects.create(
                user=user,
                address=architect_request.address,
                architect_identifier=architect_request.architect_identifier,
                architect_speciality=architect_request.architect_speciality,
                project_complexity=validated_data["project_complexity"],
                years_experience=validated_data["years_experience"],
            )

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

            email_images = settings.ACCEPT_ARCHITECT_REQUEST_IMAGES
            language_code = get_language_from_request(request)
            token = generate_password_reset_token(user.id)
            url = f"""{settings.BASE_FRONTEND_URL}/{language_code}"""
            reset_link = f"""{url}/architect/first-login/{token}"""
            signal_data = {
                "template_name": "accept_architect_request.html",
                "context": {
                    "first_name": user_data.get("first_name"),
                    "last_name": user_data.get("last_name"),
                    "email": user_data.get("email"),
                    "reset_link": reset_link,
                },
                "to_email": user_data.get("email"),
                "subject": "Accepting Architect Request",
                "images": email_images,
            }
            api_success_signal.send(sender=cls, data=signal_data)

            return True,ArchitectSerializer(architect).data,
                

    @classmethod
    def admin_refuse_architect_request(cls, pk):
        """
        Handles refusing an ArchitectRequest.

        Args:
            pk (str): The primary key of the ArchitectRequest to be refused.

        Returns:
            Response: The response object containing the result of the operation.
        """

        architect_request = ArchitectRequest.objects.get(pk=pk)
        architect_request.status = "Refused"
        architect_request.save()
        email_images = settings.REFUSE_ARCHITECT_REQUEST_IMAGES
        signal_data = {
            "template_name": "refuse_architect_request.html",
            "context": {
                "first_name": architect_request.first_name,
                "last_name": architect_request.last_name,
                "email": architect_request.email,
            },
            "to_email": architect_request.email,
            "subject": "Refusing Architect Request",
            "images": email_images,
        }
        api_success_signal.send(sender=cls, data=signal_data)

        return True,ArchitectRequestSerializer(architect_request).data
        
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

        architect_request = ArchitectRequest.objects.get(pk=pk)
        admin = Admin.objects.get(pk=admin_id)
        architect_request.meeting_responsable = admin
        architect_request.save()

        return True,ArchitectRequestSerializer(architect_request).data,
            
        
    @classmethod
    def add_note_to_architect_request(cls, architect_request_id, data):
        """
        Handles adding a note to an ArchitectRequest.

        Args:
            architect_request_id (int): The ID of the ArchitectRequest to which
            the note will be added.
            data (dict): The validated data for creating a new Note.

        Returns:
            Response: The response object containing the result of the operation.
        """

        architect_request = ArchitectRequest.objects.get(pk=architect_request_id)

        serializer = NoteSerializer(data=data)
        serializer.is_valid(raise_exception=True)

        note = Note.objects.create(
            message=serializer.validated_data["message"],
            content_object=architect_request,
        )

        return True,NoteSerializer(note).data
        
    @classmethod
    def architect_request_paginated(cls, request):
        """
        Handle GET request and return paginated ArchitectRequest objects filtered by status.

        This method retrieves ArchitectRequest objects with status 'Awaiting Demo' or 
        'Awaiting Decision', applies pagination based on the parameters in the request, 
        and returns the paginated results. If pagination is not applied correctly, it 
        returns a 400 Bad Request response.

        Args:
            request (HttpRequest): The incoming HTTP request.

        Returns:
            Response: A paginated response containing ArchitectRequest objects or an error message.
        """
        cls.update_request_statuses()
        queryset = ArchitectRequest.objects.filter(
            status__in=[AWAITING_DEMO, AWAITING_DECISION]
        ).order_by('date', 'time_slot')

        filtered_queryset = ArchitectRequestFilter(request.GET, queryset=queryset).qs
        
        paginator = cls.pagination_class()

       
        page = paginator.paginate_queryset(filtered_queryset, request)
        if page is not None:
            serializer = ArchitectRequestSerializer(page, many=True)
            return paginator.get_paginated_response(serializer.data)

       
        return Response([], status=status.HTTP_400_BAD_REQUEST)


    @classmethod
    def get_all_project_categories(cls):
        """
        Retrieve all project categories.

        This method queries the database for all ProjectCategory instances,
        serializes them, and returns them in the response.

        Returns:
            Response: A Response object containing serialized project
            categories and an HTTP 200 status.
        """
        categories = ProjectCategory.objects.all()
        serializer = ProjectCategorySerializer(categories, many=True)
        return True,serializer.data

    @classmethod
    def get_all_property_types(cls):
        """
        Retrieve all property types.

        This method queries the database for all PropertyType instances,
        serializes them, and returns them in the response.

        Returns:
            Response: A Response object containing serialized property types
             and an HTTP 200 status.
        """
        property_types = PropertyType.objects.all()
        serializer = PropertyTypeSerializer(property_types, many=True)
        return True,serializer.data

    @classmethod
    def get_all_work_types(cls):
        """
        Retrieve all work types.

        This method queries the database for all WorkType instances,
        serializes them, and returns them in the response.

        Returns:
            Response: A Response object containing serialized work types and
             an HTTP 200 status.
        """
        work_types = WorkType.objects.all()
        serializer = WorkTypeSerializer(work_types, many=True)
        return True,serializer.data

    @classmethod
    def get_all_architectural_styles(cls):
        """
        Retrieve all architectural styles.

        This method queries the database for all ArchitecturalStyle instances,
        serializes them, and returns them in the response.

        Returns:
            Response: A Response object containing serialized architectural
            styles and an HTTP 200 status.
        """
        styles = ArchitecturalStyle.objects.all()
        serializer = ArchitecturalStyleSerializer(styles, many=True)
        return True,serializer.data
    
    @classmethod
    def reschedule_architect_request(cls, architect_request_id, data):
        """
        Handles rescheduling an ArchitectRequest.

        Args:
            architect_request_id (int): The ID of the ArchitectRequest to be rescheduled.
            data (dict): The validated data for rescheduling the ArchitectRequest.

        Returns:
            Response: The response object containing the result of the operation.
        """

        serializer = ArchitectRequestRescheduleSerializer(data=data)
        serializer.is_valid(raise_exception=True)


        architect_request = ArchitectRequest.objects.get(pk=architect_request_id)
        with transaction.atomic():
            architect_request.date = serializer.validated_data.get("date")
            architect_request.time_slot = serializer.validated_data.get("time_slot")
            architect_request.clean()
            architect_request.save()

            return True, ArchitectRequestSerializer(architect_request).data
        
    @classmethod
    def get_all_time_slots(cls):
        """
        Retrieve all available time slots.

        Returns:
            Response: A Response object containing the list of time slots.
        """
        time_slots = [
            {"time": slot[0].strftime("%H:%M"), "label": slot[1]} for slot in TIME_SLOT_CHOICES
        ]
        return True,time_slots

    @classmethod
    def get_all_project_complexities(cls):
        """
        Retrieve all available project complexities.

        Returns:
            Response: A Response object containing the list of time slots.
        """
        project_complexities = [
            {"value": complexity[0], "label": complexity[1]}
            for complexity in PROJECT_COMPLEXITY_CHOICES
        ]
        return True,project_complexities

    @classmethod
    def get_all_years_experience(cls):
        """
        Retrieve all available years of experience.

        Returns:
            Response: A Response object containing the list of years of experience.
        """
        years_experience = [
            {"value": year_experience[0], "label": year_experience[1]}
            for year_experience in YEARS_EXPERIENCE_CHOICES
        ]
        return True,years_experience

    @classmethod
    def update_request_statuses(cls):
        """
        Update the status of ArchitectRequest instances based on the current date and time.
        Requests that have a meeting date and time that has passed will be updated to 'Awaiting Decision'.
        """
        now = timezone.now()
        
        # Filter requests that are still in 'Awaiting Demo' or 'Awaiting Decision' status
        requests_to_update = ArchitectRequest.objects.filter(
            Q(date__lt=now.date()) | (Q(date=now.date()) & Q(time_slot__lt=now.time()))
        )

        # Update the status of the filtered requests
        requests_to_update.update(status=AWAITING_DECISION)

        return requests_to_update.count()  # Return the number of updated requests