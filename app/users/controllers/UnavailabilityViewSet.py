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

class UnavailabilityViewSet(viewsets.ModelViewSet):
    """
    A viewset for viewing and editing Unavailability instances.


    Attributes:
        queryset (QuerySet): The queryset used for retrieving Unavailability.
        serializer_class (Type[serializers.ModelSerializer]): The serializer class used for selection data.
    """

    queryset = Unavailability.objects.all()
    serializer_class = UnavailabilitySerializer

    def create(self, request, *args, **kwargs):
        """
        Handles POST request to create a Unavailability.
        Returns:
            Response: The response object with the created Unavailability data.
        """

        try:
            unavailability = UnavailabilityService.create_unavailability(request.data,request.user)
            return Response({
                "message": "unavailability created successfully."},
                status=status.HTTP_201_CREATED
            )
        except APIException as e:
            raise e
        except Exception as e :
            raise APIException(detail=str(e))
    
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
        try:
            available_time_slots = UnavailabilityService.get_available_time_slots(request)
            return Response(available_time_slots,
                status=status.HTTP_200_OK
            )
        except APIException as e:
            raise e
        except Exception as e :
            raise APIException(detail=str(e))
    
    
        

    
