"""
This module contains viewsets for the Selection model, providing CRUD operations
for managing Meeting data via the Django REST Framework.

Classes:
    MeetingViewSet: Provides the viewset for handling operations related to the Meeting model.
"""

from rest_framework import viewsets
from app.users.models.Meeting import Meeting
from app.users.models.Architect import Architect
from app.users.serializers.MeetingSerializer import MeetingSerializer
from rest_framework import status
from rest_framework.response import Response
from app.users.services.MeetingService import MeetingService

from rest_framework.exceptions import APIException
from rest_framework.decorators import action

class MeetingViewSet(viewsets.ModelViewSet):
    """
    A viewset for viewing and editing Meeting instances.


    Attributes:
        queryset (QuerySet): The queryset used for retrieving Meeting.
        serializer_class (Type[serializers.ModelSerializer]): The serializer class used for meeting data.
    """

    queryset = Meeting.objects.all()
    serializer_class = MeetingSerializer

    def create(self, request, *args, **kwargs):
        """
        Handles POST request to create a Meeting.
        Returns:
            Response: The response object with the created Meeting data.
        """

        try:
            meeting = MeetingService.create_meeting(request.data,request.user)
            return Response(
                MeetingSerializer(meeting).data,
                status=status.HTTP_201_CREATED
            )
        except APIException as e:
            raise e
        except Exception as e :
            raise APIException(detail=str(e))
    
    @action(
        detail=False,
        methods=["GET"],
        url_path="get-admin-meetings",
    )
    def get_admin_meetings(self, request):
        """
        Custom action to get meetings by architect.

        Returns:
            Response: The list of meetings by architects.
        """
        return MeetingService.get_admin_meetings(request)
    
    @action(
        detail=False,
        methods=["GET"],
        url_path="get-daily-meetings",
    )
    def get_daily_meetings(self, request):
        """
        Custom action to get meetings by architect.

        Returns:
            Response: The list of meetings by architects.
        """
        return MeetingService.get_daily_meetings(request)