"""
Custom pagination class for Django REST Framework.

This module defines a custom pagination class that extends the default PageNumberPagination
provided by Django REST Framework. It allows for the customization of pagination parameters
such as page size through query parameters.
"""

from rest_framework.pagination import PageNumberPagination


class CustomPagination(PageNumberPagination):
    """
    Custom pagination class for handling page size via query parameters.

    This class extends the PageNumberPagination class from Django REST Framework to allow the
    customization of the page size parameter using a query parameter named 'page_size'.
    """

    page_size_query_param = "page_size"
