"""
REST API ViewSet for managing BlogThematic instances.

This module defines a ViewSet for handling CRUD operations and additional actions
related to BlogThematic instances via REST API endpoints.
"""

from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.serializers import ValidationError

from app.cms.controllers.ManageBlogPermission import ManageBlogPermission
from app.cms.models.BlogThematic import BlogThematic
from app.cms.serializers.BlogThematicSerializer import BlogThematicSerializer
from app.cms.services.BlogThematicService import BlogThematicService


class BlogThematicViewSet(viewsets.ModelViewSet):
    """
    A ViewSet for handling BlogThematic instances.

    This ViewSet provides endpoints for CRUD operations related to BlogThematic instances.
    """

    queryset = BlogThematic.objects.all()
    serializer_class = BlogThematicSerializer

    def get_queryset(self):
        """
        Get the queryset for the view.

        Raises:
            ValidationError: If the `target_user_type` query parameter is not provided.

        Returns:
            QuerySet: The filtered queryset based on the `target_user_type` parameter.
        """
        if self.action == "list":
            target_user_type = self.request.query_params.get("target_user_type")
            if not target_user_type:
                raise ValidationError("The 'target_user_type' query parameter is required.")
            return BlogThematic.objects.filter(target_user_type=target_user_type)
        else:
            return self.queryset

    def get_permissions(self):
        """
        Get the permissions that the view requires.

        All actions require the user to be authenticated.

        Returns:
            list: List of permission instances.
        """
        if self.action in ["list", "retrieve"]:
            return []
        elif self.action in ["create", "update", "partial_update", "destroy"]:
            return [IsAuthenticated(), ManageBlogPermission()]
        return super().get_permissions()

    def create(self, request, *args, **kwargs):
        """
        Create a new BlogThematic instance.

        Args:
            request (Request): The HTTP request object containing data to create
              BlogThematic instance.
            *args: Additional positional arguments.
            **kwargs: Additional keyword arguments.

        Returns:
            Response: Serialized data of the created BlogThematic instance.
        """
        return BlogThematicService.create_blog_thematic(request.data, request.user)

    def update(self, request, *args, **kwargs):
        """
        Update an existing BlogThematic instance.

        Args:
            request (Request): The HTTP request object containing data to
            update BlogThematic instance.
            *args: Additional positional arguments.
            **kwargs: Additional keyword arguments.

        Returns:
            Response: Serialized data of the updated BlogThematic instance.
        """
        partial = kwargs.pop("partial", False)
        instance = self.get_object()
        return BlogThematicService.update_blog_thematic(instance, request.data, partial=partial)

    @action(detail=True, methods=["PUT"])
    def change_visibility(self, request, pk=None):
        """
        Change the visibility of a Blog instance.

        Args:
            request (Request): The HTTP request object containing data to change visibility.
            pk (int): The primary key of the Blog instance to be updated.

        Returns:
            Response: Serialized data of the updated Blog instance.
        """

        return BlogThematicService.change_visibility(pk, request)
