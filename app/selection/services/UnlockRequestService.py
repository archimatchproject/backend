"""
UnlockRequestService Module
This module provides a service class for handling operations related to UnlockRequest objects.
It includes methods for retrieving paginated unlock requests, creating a new unlock request,
accepting an unlock request, and refusing an unlock request.
Classes:
    UnlockRequestService: A service class for managing UnlockRequest operations.
"""

from rest_framework import status
from rest_framework.response import Response

from app.core.pagination import CustomPagination
from app.selection import ACCEPTED
from app.selection import REFUSED
from app.selection.models.UnlockRequest import UnlockRequest
from app.selection.serializers.UnlockRequestSerializer import UnlockRequestSerializer


class UnlockRequestService:
    """
    Service class for handling UnlockRequest operations.

    This class provides methods to get paginated unlock requests, create an unlock request,
    accept an unlock request, and refuse an unlock request.
    """

    pagination_class = CustomPagination

    @classmethod
    def get_paginated_unlock_requests(self, request):
        """
        Handle GET request and return paginated unlock requests.

        This method retrieves all unlock requests and applies pagination based on

        Args:
            request (HttpRequest): The incoming HTTP request.

        Returns:
            Response: A paginated response containing the unlock requests,
                      or an error message if the data retrieval fails.

        Raises:
            APIException: If there is an issue with data retrieval or processing.
        """

        unlock_requests = UnlockRequest.objects.all().order_by("-created_at")
        paginator = self.pagination_class()
        page = paginator.paginate_queryset(unlock_requests, request)
        if page is not None:
            serializer = UnlockRequestSerializer(page, many=True)
            return paginator.get_paginated_response(serializer.data)
        return Response({"message": "error retrieving data"}, status=status.HTTP_400_BAD_REQUEST)

    @classmethod
    def create_unlock_request(self, selection_id, message):
        """
        Create a new unlock request.

        This method creates a new unlock request for the given selection with the provided message.

        Args:
            selection_id (int): The ID of the selection for which the unlock request
            is being created.
            message (str): The message associated with the unlock request.

        Returns:
            UnlockRequest: The created unlock request instance.

        Raises:
            APIException: If there is an issue with creating the unlock request.
        """

        UnlockRequest.objects.create(selection=selection_id, message=message)
        return True, "Unlock request created successfully."

    @classmethod
    def accept_unlock_request(self, unlock_request_id):
        """
        Accept an unlock request.

        This method updates the status of the specified unlock request to 'ACCEPTED'.

        Args:
            unlock_request_id (int): The ID of the unlock request to be accepted.

        Returns:
            UnlockRequest: The updated unlock request instance.

        Raises:
            APIException: If there is an issue with updating the unlock request.
        """

        unlock_request = UnlockRequest.objects.get(id=unlock_request_id)
        unlock_request.status = ACCEPTED
        selection = unlock_request.selection
        selection.is_blocked = False
        selection.save()
        unlock_request.save()
        return True, "Unlock request accepted successfully."

    @classmethod
    def refuse_unlock_request(self, unlock_request_id):
        """
        Refuse an unlock request.

        This method updates the status of the specified unlock request to 'REFUSED'.

        Args:
            unlock_request_id (int): The ID of the unlock request to be refused.

        Returns:
            UnlockRequest: The updated unlock request instance.

        Raises:
            APIException: If there is an issue with updating the unlock request.
        """

        unlock_request = UnlockRequest.objects.get(id=unlock_request_id)
        unlock_request.status = REFUSED
        unlock_request.save()
        return True, "Unlock request refused successfully."
