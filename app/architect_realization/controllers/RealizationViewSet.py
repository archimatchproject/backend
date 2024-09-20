"""
REST API ViewSet for managing Blog instances.

This module defines a ViewSet for handling CRUD operations and additional actions
related to Blog instances via REST API endpoints.
"""

from rest_framework import status
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.parsers import FormParser
from rest_framework.parsers import JSONParser
from rest_framework.parsers import MultiPartParser
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from app.architect_realization.models.Realization import Realization
from app.architect_realization.serializers.RealizationSerializer import RealizationPOSTSerializer
from app.architect_realization.serializers.RealizationSerializer import RealizationSerializer
from app.architect_realization.services.RealizationService import RealizationService
from app.core.pagination import CustomPagination
from app.core.exception_handler import handle_service_exceptions
from app.core.response_builder import build_response
from rest_framework import status


class RealizationViewSet(viewsets.ModelViewSet):
    """
    A ViewSet for handling Blog instances.

    This ViewSet provides endpoints for CRUD operations and additional custom actions
    related to Blog instances. It includes default actions like list, create, retrieve,
    update, and destroy, as well as a custom action for retrieving all blogs.
    """

    queryset = Realization.objects.all()
    serializer_class = RealizationSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = CustomPagination

    def get_parser_classes(self):
        """
        Get the parsers that the view requires.
        """
        if self.action not in ["realization_create"]:
            return JSONParser
        else:
            return (JSONParser, MultiPartParser, FormParser)

    def get_permissions(self):
        """
        Override this method to specify custom permissions for different actions.
        """
        if self.action in [
            "get_realizations_by_category",
            "retrieve",
            "get_realizations_by_architect",
            "get_realizations"
        ]:
            self.permission_classes = []
        return super().get_permissions()

    def get(self, request):
        """
        Handle GET request and return paginated Realization objects.

        This method retrieves all Realization objects from the database, applies
        pagination based on the parameters in the request, and returns the paginated
        results. If the pagination is not applied correctly, it returns a 400 Bad Request response.

        Args:
            request (HttpRequest): The incoming HTTP request.

        Returns:
            Response: A paginated response containing Realization objects or an error message.
        """
        queryset = Realization.objects.all()

        # Instantiate the paginator
        paginator = self.pagination_class()

        # Apply pagination to the queryset
        page = paginator.paginate_queryset(queryset, request)
        if page is not None:
            serializer = RealizationSerializer(page, many=True)
            return paginator.get_paginated_response(serializer.data)

        # If pagination is not applied correctly, return a 400 Bad Request response
        serializer = RealizationSerializer(queryset, many=True)
        return Response({"message": "error retrieving data"}, status=status.HTTP_400_BAD_REQUEST)

    @action(
        detail=False,
        url_path="create-realization",
        methods=["POST"],
        serializer_class=RealizationPOSTSerializer,
    )
    @handle_service_exceptions
    def realization_create(self, request):
        """
        Creating new realization
        """
        success,data = RealizationService.realization_create(request)
        return build_response(success=success, data=data, status=status.HTTP_201_CREATED) 

    @action(
        detail=False,
        methods=["GET"],
        permission_classes=[],
        url_path="needs",
        url_name="needs",
    )
    @handle_service_exceptions
    def get_needs(self, request):
        """
        Retrieves all  work types.

        Args:
            request (Request): HTTP request object.

        Returns:
            Response: Response containing list of work types.
        """
        success,data = RealizationService.get_architect_speciality_needs(request)
        return build_response(success=success, data=data, status=status.HTTP_200_OK)
    

    @action(
        detail=False,
        methods=["GET"],
        permission_classes=[],
        url_path="architectural-styles",
        url_name="architectural-styles",
    )
    @handle_service_exceptions
    def get_architectural_styles(self, request):
        """
        Retrieves all architectural styles.

        Args:
            request (Request): HTTP request object.

        Returns:
            Response: Response containing list of architectural styles.
        """
        success,data = RealizationService.get_architectural_styles()
        return build_response(success=success, data=data, status=status.HTTP_200_OK)


    @action(
        detail=True,
        methods=["POST"],
        url_path="get-realizations-by-category",
        serializer_class=RealizationSerializer,
    )
    @handle_service_exceptions
    def get_realizations_by_category(self, request, pk=None):
        """
        Custom action to get realizations by category.

        Args:
            request (Request): The request object containing the input data.
            pk (str): The primary key of the category to get realizations for.

        Returns:
            Response: The response object containing the realizations for the specified category.
        """
        success,data = RealizationService.get_realizations_by_category(request, pk)
        return build_response(success=success, data=data, status=status.HTTP_200_OK)


    @action(
        detail=True,
        methods=["POST"],
        url_path="get-realizations-by-architect",
        serializer_class=RealizationSerializer,
    )
    @handle_service_exceptions
    def get_realizations_by_architect(self, request, pk=None):
        """
        Custom action to get realizations by architect.

        Args:
            request (Request): The request object containing the input data.
            pk (str): The primary key of the architect to get realizations for.

        Returns:
            Response: The response object containing the realizations for the specified architect.
        """
        success,data = RealizationService.get_realizations_by_architect(request, pk)
        return build_response(success=success, data=data, status=status.HTTP_200_OK)

    @action(
        detail=True,
        url_path="update-announcement-images",
        methods=["PUT"],
    )
    @handle_service_exceptions
    def update_realization_images(self, request, pk=None):
        """
        Updating existing realization
        """
        instance = self.get_object()
        success,data = RealizationService.update_realization_images(instance, request)
        return build_response(success=success, data=data, status=status.HTTP_200_OK)


    @action(
        detail=True,
        methods=["POST"],
        url_path="get-realizations-by-category",
        serializer_class=RealizationSerializer,
    )
    @handle_service_exceptions
    def get_realizations(self, request, pk=None):
        """
        Custom action to get realizations by category.

        Args:
            request (Request): The request object containing the input data.
            pk (str): The primary key of the category to get realizations for.

        Returns:
            Response: The response object containing the realizations for the specified category.
        """
        return RealizationService.get_realizations(request, pk)
    
    
    @action(
        detail=True,
        methods=["POST"],
        url_path="get-architect-realizations",
        serializer_class=RealizationSerializer,
    )
    @handle_service_exceptions
    def get_architect_realizations(self, request, pk=None):
        """
        Custom action to get realizations by category.

        Args:
            request (Request): The request object containing the input data.
            pk (str): The primary key of the category to get realizations for.

        Returns:
            Response: The response object containing the realizations for the specified category.
        """
        return RealizationService.get_architect_realizations(request, pk)
    
    