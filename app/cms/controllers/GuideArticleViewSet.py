"""
REST API ViewSet for managing GuideArticle instances.

This module defines a ViewSet for handling CRUD operations and additional actions
related to GuideArticle instances via REST API endpoints.
"""

from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.parsers import FormParser
from rest_framework.parsers import MultiPartParser
from rest_framework.permissions import IsAuthenticated

from app.cms.controllers.ManageGuidePermission import ManageGuidePermission
from app.cms.models.GuideArticle import GuideArticle
from app.cms.serializers.GuideArticleSerializer import GuideArticleSerializer
from app.cms.services.GuideArticleService import GuideArticleService


class GuideArticleViewSet(viewsets.ModelViewSet):
    """
    A ViewSet for handling GuideArticle instances.
    """

    queryset = GuideArticle.objects.all()
    serializer_class = GuideArticleSerializer

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
        the view requires `IsAuthenticated` and `ManageGuideArticlePermission` permissions.

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
            "change_visibility",
            "upload_media",
        ]:
            return [IsAuthenticated(), ManageGuidePermission()]
        return super().get_permissions()

    def create(self, request, *args, **kwargs):
        """
        Create a new GuideArticle instance.

        Args:
            request (Request): The HTTP request object containing data to create
            GuideArticle instance.
            *args: Additional positional arguments.
            **kwargs: Additional keyword arguments.

        Returns:
            Response: Serialized data of the created GuideArticle instance.
        """
        return GuideArticleService.create_guide_article(request)

    def update(self, request, *args, **kwargs):
        """
        Update an existing GuideArticle instance.

        Args:
            request (Request): The HTTP request object containing data to update
            GuideArticle instance.
            *args: Additional positional arguments.
            **kwargs: Additional keyword arguments.

        Returns:
            Response: Serialized data of the updated GuideArticle instance.
        """
        partial = kwargs.pop("partial", False)
        instance = self.get_object()
        data = request.data
        data["partial"] = partial
        return GuideArticleService.update_guide_article(instance, data)

    @action(detail=True, methods=["PUT"])
    def change_visibility(self, request, pk=None):
        """
        Change the visibility of a GuideArticle instance.

        Args:
            request (Request): The HTTP request object containing data to change visibility.
            pk (int): The primary key of the GuideArticle instance to be updated.

        Returns:
            Response: Serialized data of the updated GuideArticle instance.
        """

        return GuideArticleService.change_visibility(pk, request)

    @action(detail=False, methods=["POST"])
    def upload_media(self, request, *args, **kwargs):
        """
        Upload media for guide-article sections.

        Args:
            request (Request): The HTTP request object containing media upload data.

        Returns:
            Response: Serialized data of the updated Blog sections.
        """
        return GuideArticleService.upload_media(request)
