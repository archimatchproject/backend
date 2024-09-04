"""
Service module for the EventDiscount model.

This module defines the service for handling the business logic and exceptions
related to EventDiscount creation and management.

Classes:
    EventDiscountService: Service class for EventDiscount operations.
"""

from django.db import transaction

from rest_framework import serializers
from rest_framework import status
from rest_framework.exceptions import APIException
from rest_framework.exceptions import NotFound
from rest_framework.response import Response

from app.core.pagination import CustomPagination
from app.subscription.models.EventDiscount import EventDiscount
from app.subscription.serializers.EventDiscountSerializer import EventDiscountSerializer
from app.users.models.Architect import Architect


class EventDiscountService:
    """
    Service class for handling EventDiscount operations.

    Handles business logic and exception handling for EventDiscount creation and management.
    """
    pagination_class = CustomPagination

    @classmethod
    def event_discount_paginated(cls, request):
        """
        Handle GET request and return paginated EventDiscount objects.

        This method retrieves all EventDiscount objects from the database, applies
        pagination based on the parameters in the request, and returns the paginated
        results. If the pagination parameters are not provided correctly or if an
        error occurs during serialization or database access, it returns a 400 Bad
        Request response with an appropriate error message.

        Args:
            request (HttpRequest): The incoming HTTP request object containing
                pagination parameters like page number, page size, etc.

        Returns:
            Response: A paginated response containing serialized EventDiscount objects
                or a 400 Bad Request response with an error message.
        """

        queryset = EventDiscount.objects.all()
        
        # Instantiate the paginator
        paginator = cls.pagination_class()

        # Apply pagination to the filtered queryset
        page = paginator.paginate_queryset(queryset, request)
        if page is not None:
            serializer = EventDiscountSerializer(page, many=True)
            return paginator.get_paginated_response(serializer.data)

        serializer = EventDiscountSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
