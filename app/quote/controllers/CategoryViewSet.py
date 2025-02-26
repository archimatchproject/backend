"""
Attributes:
    queryset (QuerySet): The queryset of Category objects.
    serializer_class (Serializer): The serializer class for Category objects.
"""

from rest_framework import status
from rest_framework import viewsets
from rest_framework.decorators import action

from app.core.exception_handler import handle_service_exceptions
from app.core.response_builder import build_response
from app.quote.models.Category import Category
from app.quote.serializers.CategorySerializer import CategorySerializer
from app.quote.services.CategoryService import CategoryService


class CategoryViewSet(viewsets.ModelViewSet):
    """
    A viewset for handling Category operations.

    This viewset provides actions to list categories, create a new category,
    and delete an existing category.
    """

    queryset = Category.objects.all()
    serializer_class = CategorySerializer

    @action(detail=False, methods=["get"])
    @handle_service_exceptions
    def get_all_categories(self, request):
        """
        Handle GET request to list all categories.

        Args:
            request (HttpRequest): The incoming HTTP request.

        Returns:
            Response: A list of all categories or an error message if retrieval fails.
        """
        success, data = CategoryService.get_all_categories()
        return build_response(success=success, data=data, status=status.HTTP_200_OK)

    @action(detail=False, methods=["post"])
    @handle_service_exceptions
    def create_category(self, request):
        """
        Handle POST request to create a new category.

        Args:
            request (HttpRequest): The incoming HTTP request.

        Returns:
            Response: The created category instance or an error message if creation fails.
        """
        success, data = CategoryService.create_category(data=request.data)
        return build_response(success=success, data=data, status=status.HTTP_201_CREATED)

    @action(detail=False, methods=["delete"])
    @handle_service_exceptions
    def delete_category(self, request, pk):
        """
        Handle DELETE request to delete a category by its ID.

        Args:
            request (HttpRequest): The incoming HTTP request.

        Returns:
            Response: A success message if the category is deleted or an error message if the category is not found.
        """
        success, message = CategoryService.delete_category(category_id=pk)
        return build_response(success=success, message=message, status=status.HTTP_200_OK)
