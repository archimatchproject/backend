"""
Module: announcement Service

This module defines the AnnouncementService class that handles announcement-related operations .

Classes:
    AnnouncementService: Service class for announcement-related operations.

"""

from datetime import datetime
from rest_framework.exceptions import NotFound, ValidationError
from app.core.pagination import CustomPagination
from app.users.models.Meeting import Meeting
from app.users.models.TimeSlot import TimeSlot
from app.users.serializers.MeetingSerializer import MeetingSerializer
from app.users.models.Admin import Admin
from rest_framework import serializers
from rest_framework import status
from rest_framework.response import Response


class MeetingService:
    """
    Service class for handling announcement-related operations .

    """
    pagination_class = CustomPagination
    @classmethod
    def create_meeting(cls, data,user):
        """
        Creates a create_meeting for a given announcement and the architect.
        Returns:
            create_meeting: The created create_meeting instance.

        Raises:
            APIException: If there are issues creating the create_meeting.
        """
        try:
            serializer = MeetingSerializer(data=data, partial=True)
            serializer.is_valid(raise_exception=True)
            meeting = Meeting.objects.create(**serializer.validated_data)
            return meeting
        except Admin.DoesNotExist as e:
            raise NotFound(detail="There is no admin for this user")
        except serializers.ValidationError as e:
            raise e

    @classmethod
    def get_admin_meetings(cls, request):
        """
        Handle GET request and return paginated Meetings objects.

        This method retrieves all Meetings objects from the database, applies
        pagination based on the parameters in the request, and returns the paginated
        results. If the pagination is not applied correctly, it returns a 400 Bad Request response.

        Args:
            request (HttpRequest): The incoming HTTP request.

        Returns:
            Response: A paginated response containing Meetings objects or an error message.
        """
        try:
            user = request.user
            queryset = Meeting.objects.filter(admin__user=user)
            
            paginator = cls.pagination_class()
            page = paginator.paginate_queryset(queryset, request)
            if page is not None:
                serializer = MeetingSerializer(page, many=True)
                return paginator.get_paginated_response(serializer.data)
            
            serializer = MeetingSerializer(queryset, many=True)
        except Meeting.DoesNotExist as e:
            raise NotFound(detail="Meeting not foun")
        except serializers.ValidationError as e:
            raise e
        return Response(
            serializer.data,
            status=status.HTTP_200_OK,
        )