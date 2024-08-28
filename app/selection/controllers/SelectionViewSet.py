# app/announcement/selection_viewsets.py

"""
This module contains viewsets for the Selection model, providing CRUD operations
for managing selection data via the Django REST Framework.

Classes:
    SelectionViewSet: Provides the viewset for handling operations related to the Selection model.
"""

from rest_framework import viewsets
from app.selection.models.Selection import Selection
from app.selection.serializers.SelectionSerializer import SelectionSerializer,SelectionPostSerializer
from app.users.models.Architect import Architect
from app.announcement.models.Announcement import Announcement
from rest_framework import status
from rest_framework.response import Response
from app.selection.services.SelectionService import SelectionService
from rest_framework.exceptions import APIException

class SelectionViewSet(viewsets.ModelViewSet):
    """
    A viewset for viewing and editing Selection instances.


    Attributes:
        queryset (QuerySet): The queryset used for retrieving selections.
        serializer_class (Type[serializers.ModelSerializer]): The serializer class used for selection data.
    """

    queryset = Selection.objects.all()
    serializer_class = SelectionSerializer

    def create(self, request, *args, **kwargs):
        """
        Handles POST request to create a selection.

        Args:
            request (Request): The request object containing announcement_id.

        Returns:
            Response: The response object with the created selection data.
        """

        try:
            selection = SelectionService.create_selection(request.data,request.user)
            return Response({"detail": "Selection created successfully.", "selection": SelectionSerializer(selection).data}, status=status.HTTP_201_CREATED)
        except APIException as e:
            raise e
        except Exception as e :
            raise APIException(detail=str(e))
        

    
