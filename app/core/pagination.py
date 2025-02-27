"""
Pagination class for paginating responses from the server and returning results
to the client using the specified pagination method
"""

from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response


class CustomPagination(PageNumberPagination):
    """
    Custom pagination class for handling page size via query parameters.

    This class extends the PageNumberPagination class from Django REST Framework to allow the
    customization of the page size parameter using a query parameter named 'page_size'.
    """

    page_size_query_param = "page_size"

    def get_paginated_response(self, data):
        """
        Override the method to include totalPages, count, next, and previous in the response.

        Args:
            data (list): List of serialized objects.

        Returns:
            Response: A Response object with paginated
            results and additional pagination information.
        """
        response = Response(
            {
                "count": self.page.paginator.count,
                "next": self.get_next_link(),
                "previous": self.get_previous_link(),
                "totalPages": self.page.paginator.num_pages,
                "results": data,
            }
        )
        response["X-Pagination"] = "true"
        return response
