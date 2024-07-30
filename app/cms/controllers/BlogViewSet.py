"""
REST API ViewSet for managing Blog instances.

This module defines a ViewSet for handling CRUD operations and additional actions
related to Blog instances via REST API endpoints.
"""

from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.parsers import FormParser
from rest_framework.parsers import MultiPartParser
from rest_framework.permissions import IsAuthenticated

from app.cms.controllers.ManageBlogPermission import ManageBlogPermission
from app.cms.models.Blog import Blog
from app.cms.serializers.BlogSerializer import BlogSerializer
from app.cms.services.BlogService import BlogService


class BlogViewSet(viewsets.ModelViewSet):
    """
    A ViewSet for handling Blog instances.

    This ViewSet provides endpoints for CRUD operations related to Blog instances.
    """

    queryset = Blog.objects.all()
    serializer_class = BlogSerializer

    def get_parser_classes(self):
        """
        Get the parsers that the view requires.
        """
        if self.action in ["update_cover_photo", "upload_media"]:
            return (MultiPartParser, FormParser)
        return super().get_parser_classes()

    def get_permissions(self):
        """
        Get the permissions that the view requires.

        For `list` and `retrieve` actions (`GET` requests), no specific permissions are required.
        For `create`, `update`, `partial_update`, and `destroy` actions
        (`POST`, `PUT`, `PATCH`, `DELETE` requests),
        the view requires `IsAuthenticated` and `ManageBlogPermission` permissions.

        Returns:
            list: List of permission instances.
        """
        if self.action in ["list", "retrieve"]:
            return []
        elif self.action in [
            "create",
            "update",
            "partial_update",
            "destroy",
            "update_cover_photo",
            "change_visibility",
            "upload_media",
        ]:
            return [IsAuthenticated(), ManageBlogPermission()]
        return super().get_permissions()

    def create(self, request, *args, **kwargs):
        """
        Create a new Blog instance.

        Args:
            request (Request): The HTTP request object containing data to create Blog instance.
            *args: Additional positional arguments.
            **kwargs: Additional keyword arguments.

        Returns:
            Response: Serialized data of the created Blog instance.
        """
        return BlogService.create_blog(request.data, request.user)

    def update(self, request, *args, **kwargs):
        """
        Update an existing Blog instance.

        Args:
            request (Request): The HTTP request object containing data to update Blog instance.
            *args: Additional positional arguments.
            **kwargs: Additional keyword arguments.

        Returns:
            Response: Serialized data of the updated Blog instance.
        """
        partial = kwargs.pop("partial", False)
        instance = self.get_object()
        return BlogService.update_blog(instance, request.data, partial=partial)

    @action(detail=True, methods=["PUT"])
    def update_cover_photo(self, request, pk=None):
        """
        Update an existing Blog cover_photo.

        Args:
            request (Request): The HTTP request object containing data to update Blog instance.
            pk (int): The primary key of the Blog instance to be updated.

        Returns:
            Response: Serialized data of the updated Blog instance.
        """
        return BlogService.update_cover_photo(pk, request)

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

        return BlogService.change_visibility(pk, request)

    @action(detail=False, methods=["POST"])
    def upload_media(self, request, *args, **kwargs):
        """
        Upload media for blog sections.

        Args:
            request (Request): The HTTP request object containing media upload data.

        Returns:
            Response: Serialized data of the updated Blog sections.
        """
        return BlogService.upload_media(request)

    @action(detail=False, methods=["GET"])
    def list_tags(self, request):
        """
        Retrieve all tags.
        """
        return BlogService.list_tags()
