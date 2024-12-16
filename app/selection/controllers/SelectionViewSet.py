# app/announcement/selection_viewsets.py

"""
This module contains viewsets for the Selection model, providing CRUD operations
for managing selection data via the Django REST Framework.

Classes:
    SelectionViewSet: Provides the viewset for handling operations related to the Selection model.
"""
from rest_framework.decorators import action
from rest_framework import viewsets
from app.selection.models.Selection import Selection
from app.selection.serializers.SelectionSerializer import SelectionSerializer,SelectionPostSerializer
from rest_framework import status
from app.selection.services.SelectionService import SelectionService
from app.core.exception_handler import handle_service_exceptions
from app.core.response_builder import build_response
from rest_framework import status
from rest_framework.serializers import ValidationError

from app.users.models.Architect import Architect
class SelectionViewSet(viewsets.ModelViewSet):
    """
    A viewset for viewing and editing Selection instances.


    Attributes:
        queryset (QuerySet): The queryset used for retrieving selections.
        serializer_class (Type[serializers.ModelSerializer]): The serializer class used for selection data.
    """

    queryset = Selection.objects.all()
    serializer_class = SelectionSerializer

    @handle_service_exceptions
    def create(self, request, *args, **kwargs):
        """
        Handles POST request to create a selection.

        Args:
            request (Request): The request object containing announcement_id.

        Returns:
            Response: The response object with the created selection data.
        """

        success,data = SelectionService.create_selection(request.data,request.user)
        return build_response(success=success, data=data, status=status.HTTP_201_CREATED)
    
    
    @action(
        detail=True,
        url_path="announcement-selections",
        methods=["GET"],
    )
    @handle_service_exceptions
    def get_announcement_selections(self, request, pk=None):
        """
        Retrieves selections for a given announcement and updates announcement images.

        Args:
            request (Request): The request object containing any necessary data for the update.
            pk (int, optional): The primary key of the announcement for which selections are retrieved. 

        Returns:
            Response: The response object indicating success and containing the data of the selections,
                    or an error message if the operation fails.
        """
        success,data = SelectionService.get_announcement_selections(pk)
        return build_response(success=success, data=data, status=status.HTTP_200_OK)
    
    @action(detail=False, methods=["GET"], url_path="architect-selections")
    @handle_service_exceptions
    def get_architect_selections(self, request):
        """
        Retrieves all selections made by the authenticated architect.

        Args:
            request (Request): The request object containing the architect's user information.

        Returns:
            Response: The response object with the list of selections made by the architect.
        """
        
        return SelectionService.get_selections_by_architect(request)
        
    
    @action(detail=True, methods=["PUT"], url_path="update-name")
    @handle_service_exceptions
    def update_selection_name(self, request, pk=None):
        """
        Updates the name of the given selection.

        Args:
            request (Request): The request object containing the new name.
            pk (int): The primary key of the selection to update.

        Returns:
            Response: The response object with the updated selection data.
        """
        name = request.data.get("name",False)
        if not name :
            raise ValidationError(detail="the selection name is not provided")
        success, data = SelectionService.update_selection_name(pk, name)
        return build_response(success=success, data=data, status=status.HTTP_200_OK)
        
    @action(detail=True, methods=['POST'], url_path='confirm-discussion-phase')
    @handle_service_exceptions
    def confirm_discussion_phase(self, request, pk=None):
        """
        Endpoint to confirm the completion of the discussion phase (phase 1) and progress to phase 2.

        Args:
            pk (int): The ID of the selection to update.

        Returns:
            Response: The updated selection and phase data or an error message.
        """

        success, message = SelectionService.confirm_discussion_phase(selection_id=pk)
        return build_response(success=success, message=message, status=status.HTTP_200_OK)    
    
    def get(self, request):
        """
        Handle GET request and return paginated Selections objects.

        This method retrieves all Selections objects from the database, applies
        pagination based on the parameters in the request, and returns the paginated
        results. If the pagination is not applied correctly, it returns a 400 Bad Request response.

        Args:
            request (HttpRequest): The incoming HTTP request.

        Returns:
            Response: A paginated response containing Selections objects or an error message.
        """
        return SelectionService.get_selections(request)
    
    @action(detail=True, methods=['PUT'], url_path='abandon-selection')
    @handle_service_exceptions
    def abandon_selection(self, request, pk=None):
        """
        Endpoint to abandon the selection by an architect

        Args:
            pk (int): The ID of the selection to update.

        Returns:
            Response: a success or an error message.
        """

        success, message = SelectionService.abandon_selection(selection_id=pk)
        return build_response(success=success, message=message, status=status.HTTP_200_OK)  
    
    @action(detail=True, methods=['GET'], url_path='not-selected-announcements')
    @handle_service_exceptions
    def get_not_selected_announcements(self, request, pk=None):
        """
        Handle GET request and return paginated not selected announcements objects.

        This method retrieves all not selected announcements objects from the database, applies
        pagination based on the parameters in the request, and returns the paginated
        results. If the pagination is not applied correctly, it returns a 400 Bad Request response.

        Args:
            request (HttpRequest): The incoming HTTP request.

        Returns:
            Response: A paginated response containing not selected announcements objects or an error message.
        """

        return SelectionService.get_not_selected_announcements(request)
        
    @action(detail=True, methods=['POST'], url_path='broadcast-announcement')
    @handle_service_exceptions
    def broadcast_announcement(self, request, pk=None):
        """
        Endpoint to broadcast the announcement

        Args:
            pk (int): The ID of the announcement to update.

        Returns:
            Response: a success or an error message.
        """

        success, message = SelectionService.broadcast_announcement(announcement_id=pk)
        return build_response(success=success, message=message, status=status.HTTP_200_OK)  
    
    @action(detail=True, methods=['GET'], url_path='not-selected-announcements')
    @handle_service_exceptions
    def get_discussion_phase_selections(self, request):
        """
        Handle GET request and return paginated not selected announcements objects.

        This method retrieves all not selected announcements objects that are in the
        'DISCUSSION' phase and have 3, 2, 1, or 0 days left until the limit date. Pagination is applied
        based on the parameters in the request.

        Args:
            request (HttpRequest): The incoming HTTP request.

        Returns:
            Response: A paginated response containing the filtered selections or an error message.
        """

        return SelectionService.get_discussion_phase_selections(request)
    
    @action(detail=True, methods=['GET'], url_path='selection-logs')
    @handle_service_exceptions
    def get_selection_logs(self, request, pk=None):
        """
        Retrieve the action logs associated with a specific selection.

        This endpoint fetches the logs for the given selection ID (pk) and returns 
        the serialized log data. It utilizes the `SelectionService.get_selection_logs` 
        method to perform the retrieval.

        Args:
            request (Request): The incoming HTTP request object.
            pk (int): The ID of the selection for which to retrieve action logs.

        Returns:
            Response: A JSON response containing:
                - `success` (bool): Indicates whether the operation was successful.
                - `data` (list): Serialized list of action logs for the selection.
                - HTTP 200 OK: Returned upon successful retrieval.
            
        Raises:
            APIException: If no logs are found or an internal error occurs.
        """

        success, data = SelectionService.get_selection_logs(selection_id=pk)
        return build_response(success=success, data=data, status=status.HTTP_200_OK)
    
    
    @action(detail=True, methods=['POST'], url_path='broadcast-selection-announcement')
    @handle_service_exceptions
    def broadcast_selection_announcement(self, request, pk=None):
        """
        Endpoint to broadcast the announcement

        Args:
            pk (int): The ID of the selection to update.

        Returns:
            Response: a success or an error message.
        """

        success, message = SelectionService.broadcast_selection_announcement(selection_id=pk,user=request.user)
        return build_response(success=success, message=message, status=status.HTTP_200_OK)  
    
    @action(detail=True, methods=['POST'], url_path='block-selection')
    @handle_service_exceptions
    def block_selection(self, request, pk=None):
        """
        Endpoint to to block selection

        Args:
            pk (int): The ID of the selection to update.

        Returns:
            Response: a success or an error message.
        """

        success, message = SelectionService.block_selection(selection_id=pk,user=request.user)
        return build_response(success=success, message=message, status=status.HTTP_200_OK)  
    
    @action(detail=True, methods=['POST'], url_path='change-selection-deadline')
    @handle_service_exceptions
    def change_selection_deadline(self, request, pk=None):
        """
        change the selection deadline

        Args:
            pk (int): The ID of the selection to update.

        Returns:
            Response: a success or an error message.
        """

        success, message = SelectionService.change_selection_deadline(selection_id=pk,user=request.user,data=request.data)
        return build_response(success=success, message=message, status=status.HTTP_200_OK)  
    
    @action(detail=True, methods=['POST'], url_path='confirm-discussion-phase-admin')
    @handle_service_exceptions
    def confirm_discussion_phase_admin(self, request, pk=None):
        """
        Endpoint to confirm the completion of the discussion phase (phase 1) and progress to phase 2.

        Args:
            pk (int): The ID of the selection to update.

        Returns:
            Response: The updated selection and phase data or an error message.
        """

        success, message = SelectionService.confirm_discussion_phase_admin(selection_id=pk,user=request.user)
        return build_response(success=success, message=message, status=status.HTTP_200_OK)    
    
    @action(detail=True, methods=['POST'], url_path='cancel-selection')
    @handle_service_exceptions
    def cancel_selection(self, request, pk=None):
        """
        Endpoint to confirm the completion of the discussion phase (phase 1) and progress to phase 2.

        Args:
            pk (int): The ID of the selection to update.

        Returns:
            Response: The updated selection and phase data or an error message.
        """

        success, message = SelectionService.cancel_selection(selection_id=pk,user=request.user)
        return build_response(success=success, message=message, status=status.HTTP_200_OK)    