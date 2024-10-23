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
        
        architect = Architect.objects.get(user=request.user)
        success, data = SelectionService.get_selections_by_architect(architect)
        return build_response(success=success, data=data, status=status.HTTP_200_OK)
    
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
    
