"""
CategoryService Module
This module provides a service class for handling operations related to Category objects.
It includes methods for creating a category, retrieving all categories, and deleting a category.

Classes:
    CategoryService: A service class for managing Category operations.
"""

from rest_framework.exceptions import APIException

from app.quote.models.Category import Category
from app.quote.serializers.CategorySerializer import CategorySerializer


class CategoryService:
    """
    Service class for handling Category operations.

    This class provides methods to create a category, retrieve all categories, and delete a category.
    """

    @classmethod
    def get_all_categories(cls):
        """
        Retrieve and return a list of all categories.

        Args:
            None

        Returns:
            tuple: (True, data) where data is a list of category data.
        """
        categories = Category.objects.all().order_by("-created_at")
        serializer = CategorySerializer(categories, many=True)
        return True, serializer.data

    @classmethod
    def create_category(cls, data):
        """
        Create a new category.

        Args:
            data (dict): The data for the new category, including the title.

        Returns:
            tuple: (True, data) where data is a success message or category information.

        Raises:
            APIException: If there is an issue with creating the category.
        """
        title = data.get("title")
        if title is None:
            raise APIException("Title is required to create a category.")

        category = Category.objects.create(title=title)
        category_data = CategorySerializer(category).data
        return True, category_data

    @classmethod
    def delete_category(cls, category_id):
        """
        Delete a category by its ID.

        Args:
            category_id (int): The ID of the category to be deleted.

        Returns:
            tuple: (True, data) where data is a success message or an error message if the category was not found.

        Raises:
            APIException: If there is an issue with deleting the category or if the category is not found.
        """
        try:
            category = Category.objects.get(id=category_id)
            category.delete()
            return True, "Category deleted successfully."
        except Category.DoesNotExist:
            raise APIException("Category not found.")
