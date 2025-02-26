"""
Attributes:
    queryset (QuerySet): The queryset of QuoteService objects.
    serializer_class (Serializer): The serializer class for QuoteService objects.
"""

from rest_framework import status
from rest_framework import viewsets
from rest_framework.decorators import action

from app.core.exception_handler import handle_service_exceptions
from app.core.response_builder import build_response
from app.quote.models.QuoteService import QuoteService
from app.quote.serializers.QuoteServiceSerializer import QuoteServiceSerializer
from app.quote.services.QuoteServiceService import QuoteServiceService


class QuoteServiceViewSet(viewsets.ModelViewSet):
    """
    A viewset for handling QuoteService operations.

    This viewset provides actions to get all quote services, create a quote service,
    update a quote service, and delete a quote service.
    """

    queryset = QuoteService.objects.all()
    serializer_class = QuoteServiceSerializer

    @action(detail=False, methods=["get"])
    @handle_service_exceptions
    def get_all_quote_services(self, request):
        """
        Handle GET request to list all quote services.

        Args:
            request (HttpRequest): The incoming HTTP request.

        Returns:
            Response: A paginated response containing the quote services,
                      or an error message if data retrieval fails.
        """
        return QuoteServiceService.get_all_quote_services(request=request)

    @action(detail=False, methods=["post"])
    @handle_service_exceptions
    def create_quote_service(self, request):
        """
        Handle POST request to create a new quote service.

        Args:
            request (HttpRequest): The incoming HTTP request.

        Returns:
            Response: The created quote service instance,
                      or an error message if creation fails.
        """
        success, data = QuoteServiceService.create_quote_service(data=request.data)
        return build_response(success=success, data=data, status=status.HTTP_201_CREATED)

    @action(detail=False, methods=["put"])
    @handle_service_exceptions
    def update_quote_service(self, request, pk):
        """
        Handle PUT request to update an existing quote service.

        Args:
            request (HttpRequest): The incoming HTTP request.

        Returns:
            Response: The updated quote service instance,
                      or an error message if the update fails.
        """
        success, data = QuoteServiceService.update_quote_service(data=request.data, pk=pk)
        return build_response(success=success, data=data, status=status.HTTP_200_OK)

    @action(detail=False, methods=["delete"])
    @handle_service_exceptions
    def delete_quote_service(self, request, pk):
        """
        Handle DELETE request to delete a quote service.

        Args:
            request (HttpRequest): The incoming HTTP request.

        Returns:
            Response: A success message if the quote service is deleted,
                      or an error message if the deletion fails.
        """
        success, message = QuoteServiceService.delete_quote_service(quote_service_id=pk)
        return build_response(success=success, message=message, status=status.HTTP_200_OK)
