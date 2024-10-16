"""
This module contains viewsets for the Selection model, providing CRUD operations
for managing Unavailability data via the Django REST Framework.

Classes:
    UnavailabilityViewSet: Provides the viewset for handling operations related to the Unavailability model.
"""

from rest_framework import viewsets
from app.users.models.Unavailability import Unavailability
from app.users.models.Architect import Architect
from app.users.serializers.UnavailabilitySerializer import UnavailabilitySerializer
from rest_framework import status
from rest_framework.response import Response
from app.users.services.UnavailabilityService import UnavailabilityService
from rest_framework.exceptions import APIException
from rest_framework.decorators import action
from app.core.exception_handler import handle_service_exceptions
from app.core.response_builder import build_response
from rest_framework import status
class UnavailabilityViewSet(viewsets.ModelViewSet):
    """
    A viewset for viewing and editing Unavailability instances.


    Attributes:
        queryset (QuerySet): The queryset used for retrieving Unavailability.
        serializer_class (Type[serializers.ModelSerializer]): The serializer class used for selection data.
    """

    queryset = Unavailability.objects.all()
    serializer_class = UnavailabilitySerializer

    @handle_service_exceptions
    def create(self, request, *args, **kwargs):
        """
        Handles POST request to create a Unavailability.
        Returns:
            Response: The response object with the created Unavailability data.
        """

        
        success,message = UnavailabilityService.create_unavailability(request.data,request.user)
        return build_response(success=success, message=message, status=status.HTTP_201_CREATED)
        
    
    @action(
        detail=True,
        methods=["GET"],
        url_path="available-time-slots",
        url_name="available-time-slots",
    )
    def get_available_time_slots(self, request):
        """
        Retrieves Architect details.

        Args:
            self (ArchitectViewSet): Instance of the ArchitectViewSet class.
            request (Request): HTTP request object.

        Returns:
            Response: Response containing Architect details.
        """
        
        success,available_time_slots = UnavailabilityService.get_available_time_slots(request)
        build_response(success=success, data=available_time_slots, status=status.HTTP_200_OK)

    
    
        

    
