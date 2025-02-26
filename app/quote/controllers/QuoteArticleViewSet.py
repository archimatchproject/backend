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
from app.quote.models.QuoteArticle import QuoteArticle
from app.quote.serializers.QuoteArticleSerializer import QuoteArticleSerializer
from app.quote.services.QuoteArticleService import QuoteArticleService


class QuoteArticleViewSet(viewsets.ModelViewSet):
    """
    A viewset for handling UnlockRequest operations.

    This viewset provides actions to get paginated unlock requests, create an unlock request,
    accept an unlock request, and refuse an unlock request.
    """

    queryset = QuoteArticle.objects.all()
    serializer_class = QuoteArticleSerializer

    @action(detail=False, methods=["get"])
    @handle_service_exceptions
    def get_all_quoteArticles(self, request):
        """
        Handle GET request to list paginated quoteArticles.

        Args:
            request (HttpRequest): The incoming HTTP request.

        Returns:
            Response: A paginated response containing the quoteArticles,
                      or an error message if the data retrieval fails.
        """
        return QuoteArticleService.get_all_quoteArticles(request)

    @action(detail=False, methods=["post"])
    @handle_service_exceptions
    def create_quoteArticle(self, request):
        """
        Handle POST request to create a new quoteArticles.

        Args:
            request (HttpRequest): The incoming HTTP request.

        Returns:
            Response: The created quoteArticles instance,
                      or an error message if the creation fails.
        """

        success, message = QuoteArticleService.create_quoteArticle(data=request)

        return build_response(success=success, message=message, status=status.HTTP_201_CREATED)

    @action(detail=False, methods=["update"])
    @handle_service_exceptions
    def update_quoteArticle(self, request, pk):
        """
        Handle POST request to update a quoteArticles.

        Args:
            request (HttpRequest): The incoming HTTP request.

        Returns:
            Response: The updated quoteArticles instance,
                      or an error message if the creation fails.
        """

        success, message = QuoteArticleService.update_quoteArticle(data=request, pk=pk)

        return build_response(success=success, message=message, status=status.HTTP_201_CREATED)

    @action(detail=False, methods=["delete"])
    @handle_service_exceptions
    def delete_quoteArticle(self, request, pk):
        """
        Handle POST request to delete a quoteArticle.

        Args:
            request (HttpRequest): The incoming HTTP request.

        Returns:
            Response: The deleted quoteArticle instance,
                      or an error message if the creation fails.
        """

        success, message = QuoteArticleService.delete_quoteArticle(quoteArticle_id=pk)

        return build_response(success=success, message=message, status=status.HTTP_200_OK)
