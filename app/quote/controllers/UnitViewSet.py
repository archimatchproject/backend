"""
Attributes:
    queryset (QuerySet): The queryset of Unit objects.
    serializer_class (Serializer): The serializer class for Unit objects.
"""

from rest_framework import status
from rest_framework import viewsets
from rest_framework.decorators import action

from app.core.exception_handler import handle_service_exceptions
from app.core.response_builder import build_response
from app.quote.models.Unit import Unit
from app.quote.serializers.UnitSerializer import UnitSerializer
from app.quote.services.UnitService import UnitService


class UnitViewSet(viewsets.ModelViewSet):
    """
    A viewset for handling UnlockRequest operations.

    This viewset provides actions to get paginated unlock requests, create an unlock request,
    accept an unlock request, and refuse an unlock request.
    """

    queryset = Unit.objects.all()
    serializer_class = UnitSerializer

    @action(detail=False, methods=["get"])
    @handle_service_exceptions
    def get_all_units(self, request):
        """
        Handle GET request to list paginated units.

        Args:
            request (HttpRequest): The incoming HTTP request.

        Returns:
            Response: A paginated response containing the units,
                      or an error message if the data retrieval fails.
        """
        success, data = UnitService.get_all_units()
        return build_response(success=success, data=data, status=status.HTTP_200_OK)

    @action(detail=False, methods=["post"])
    @handle_service_exceptions
    def create_unit(self, request):
        """
        Handle POST request to create a new units.

        Args:
            request (HttpRequest): The incoming HTTP request.

        Returns:
            Response: The created units instance,
                      or an error message if the creation fails.
        """

        success, message = UnitService.create_unit(data=request.data)

        return build_response(success=success, message=message, status=status.HTTP_201_CREATED)

    @action(detail=False, methods=["post"])
    @handle_service_exceptions
    def delete_unit(self, request, pk):
        """
        Handle POST request to delete a unit.

        Args:
            request (HttpRequest): The incoming HTTP request.

        Returns:
            Response: The deleted unit instance,
                      or an error message if the creation fails.
        """

        success, message = UnitService.delete_unit(unit_id=pk)

        return build_response(success=success, message=message, status=status.HTTP_200_OK)
