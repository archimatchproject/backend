"""
QuoteServiceService Module
This module provides a service class for handling operations related to QuoteService objects.
It includes methods for creating a quote service, retrieving all quote services, and deleting a quote service.

Classes:
    QuoteServiceService: A service class for managing QuoteService operations.
"""

from rest_framework import status
from rest_framework.exceptions import APIException
from rest_framework.response import Response

from app.core.pagination import CustomPagination
from app.quote.filters.QuoteServiceFilter import QuoteServiceFilter
from app.quote.models.QuoteService import QuoteService
from app.quote.serializers.QuoteServiceSerializer import QuoteServiceInputSerializer
from app.quote.serializers.QuoteServiceSerializer import QuoteServiceSerializer
from app.users.models.Architect import Architect


class QuoteServiceService:
    """
    Service class for handling QuoteService operations.

    This class provides methods to create a quote service, retrieve all quote services, and delete a quote service.
    """

    pagination_class = CustomPagination

    @classmethod
    def get_all_quote_services(cls, request):
        """
        Retrieve and return a list of all quote services.

        Args:
            None

        Returns:
            tuple: (True, data) where data is a list of quote service data.
        """

        user = request.user
        architect = Architect.objects.get(user=user)
        queryset = QuoteService.objects.filter(architect=architect).order_by("-created_at")
        filtered_queryset = QuoteServiceFilter(request.GET, queryset=queryset).qs
        paginator = cls.pagination_class()
        page = paginator.paginate_queryset(filtered_queryset, request)
        if page is not None:
            serializer = QuoteServiceSerializer(page, many=True)
            return paginator.get_paginated_response(serializer.data)

        return Response([], status=status.HTTP_400_BAD_REQUEST)

    @classmethod
    def create_quote_service(cls, request):
        """
        Create a new quote service.

        Args:
            data (dict): The data for the new quote service, including title, description, unit, category,
            and unit price.

        Returns:
            tuple: (True, data) where data is the created quote service information.

        Raises:
            APIException: If there is an issue with creating the quote service.
        """

        serialiser = QuoteServiceInputSerializer(data=request.data)
        validated_data = serialiser.is_valid(raise_exception=True)
        user = request.user
        architect = Architect.objects.get(user=user)
        if QuoteService.objects.filter(title=validated_data.get("title")).exists():
            raise APIException("Service with this title already exists.")
        quote_service = QuoteService.objects.create(architect=architect, **validated_data)
        quoteArticle_data = QuoteServiceSerializer(quote_service).data
        return True, quoteArticle_data

    @classmethod
    def update_quote_service(cls, data, pk):
        """
        Updates an existing QuoteService instance with the provided data.
        Args:
            cls: The class that calls this method.
            data (dict): The data to update the QuoteService instance with.
            pk (int): The primary key of the QuoteService instance to update.
        Returns:
            tuple: A tuple containing a boolean indicating success and a message.
        Raises:
            APIException: If the QuoteService instance is not found.
        """

        quote_service = QuoteService.objects.get(id=pk)
        if not quote_service:
            raise APIException("Service not found.")
        serialiser = QuoteServiceInputSerializer(quote_service, data=data, partial=True)
        serialiser.is_valid(raise_exception=True)
        quote_service = serialiser.save()
        return True, "Article updated successfully."

    @classmethod
    def delete_quote_service(cls, service_id):
        """
        Delete a quoteService by its ID.

        Args:
            quoteService_id (int): The ID of the quoteService to be deleted.

        Returns:
            tuple: (True, data) where data is a success message or an error message if the quoteService was not found.

        Raises:
            APIException: If there is an issue with deleting the quoteService or if the quoteService is not found.
        """
        try:
            quote_service = QuoteService.objects.get(id=service_id)
            quote_service.delete()
            return True, "Article deleted successfully."
        except QuoteService.DoesNotExist:
            raise APIException("Article not found.")
