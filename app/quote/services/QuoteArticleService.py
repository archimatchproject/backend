"""
QuoteArticleService Module
This module provides a service class for handling operations related to Unit objects.
It includes methods for creating a unit, retrieving all units, and deleting a unit.

Classes:
    QuoteArticleService: A service class for managing Unit operations.
"""

from rest_framework import status
from rest_framework.exceptions import APIException
from rest_framework.response import Response

from app.core.pagination import CustomPagination
from app.quote.filters.QuoteArticleFilter import QuoteArticleFilter
from app.quote.models.QuoteArticle import QuoteArticle
from app.quote.serializers.QuoteArticleSerializer import QuoteArticleInputSerializer
from app.quote.serializers.QuoteArticleSerializer import QuoteArticleSerializer
from app.users.models.Architect import Architect


class QuoteArticleService:
    """
    Service class for handling Unit operations.

    This class provides methods to create a unit, retrieve all units, and delete a unit.
    """

    pagination_class = CustomPagination

    @classmethod
    def get_all_quoteArticles(cls, request):
        """
        Retrieve and return a paginated list of all units.

        Args:
            request (HttpRequest): The incoming HTTP request.

        Returns:
            tuple: (True, data) where data is a list of paginated unit data.
        """
        user = request.user
        architect = Architect.objects.get(user=user)
        queryset = QuoteArticle.objects.filter(architect=architect).order_by("-created_at")
        filtered_queryset = QuoteArticleFilter(request.GET, queryset=queryset).qs
        paginator = cls.pagination_class()
        page = paginator.paginate_queryset(filtered_queryset, request)
        if page is not None:
            serializer = QuoteArticleSerializer(page, many=True)
            return paginator.get_paginated_response(serializer.data)

        return Response([], status=status.HTTP_400_BAD_REQUEST)

    @classmethod
    def create_quoteArticle(cls, request):
        """
        Create a new quoteArticle.

        Args:
            title (str): The title for the new quoteArticle.

        Returns:
            tuple: (True, data) where data is a success message or quoteArticle information.

        Raises:
            APIException: If there is an issue with creating the quoteArticle.
        """

        serialiser = QuoteArticleInputSerializer(data=request.data)
        validated_data = serialiser.is_valid(raise_exception=True)
        user = request.user
        architect = Architect.objects.get(user=user)
        if QuoteArticle.objects.filter(title=validated_data.get("title")).exists():
            raise APIException("QuoteArticle with this title already exists.")
        quoteArticle = QuoteArticle.objects.create(architect=architect, **validated_data)
        quoteArticle_data = QuoteArticleSerializer(quoteArticle).data
        return True, quoteArticle_data

    @classmethod
    def update_quoteArticle(cls, data, pk):
        """
        Updates an existing QuoteArticle instance with the provided data.
        Args:
            cls: The class that calls this method.
            data (dict): The data to update the QuoteArticle instance with.
            pk (int): The primary key of the QuoteArticle instance to update.
        Returns:
            tuple: A tuple containing a boolean indicating success and a message.
        Raises:
            APIException: If the QuoteArticle instance is not found.
        """

        quoteArticle = QuoteArticle.objects.get(id=pk)
        if not quoteArticle:
            raise APIException("Article not found.")
        serialiser = QuoteArticleInputSerializer(quoteArticle, data=data, partial=True)
        serialiser.is_valid(raise_exception=True)
        quoteArticle = serialiser.save()
        return True, "Article updated successfully."

    @classmethod
    def delete_quoteArticle(cls, quoteArticle_id):
        """
        Delete a quoteArticle by its ID.

        Args:
            quoteArticle_id (int): The ID of the quoteArticle to be deleted.

        Returns:
            tuple: (True, data) where data is a success message or an error message if the quoteArticle was not found.

        Raises:
            APIException: If there is an issue with deleting the quoteArticle or if the quoteArticle is not found.
        """
        try:
            quoteArticle = QuoteArticle.objects.get(id=quoteArticle_id)
            quoteArticle.delete()
            return True, "Article deleted successfully."
        except QuoteArticle.DoesNotExist:
            raise APIException("Article not found.")
