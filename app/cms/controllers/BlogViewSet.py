"""
REST API ViewSet for managing Blog instances.

This module defines a ViewSet for handling CRUD operations and additional actions
related to Blog instances via REST API endpoints.
"""

from rest_framework import permissions
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from app.cms.controllers.utils.ManageBlogPermission import ManageBlogPermission
from app.cms.models.Blog import Blog
from app.cms.serializers.BlogSerializer import BlogSerializer


class BlogViewSet(viewsets.ModelViewSet):
    """
    A ViewSet for handling Blog instances.

    This ViewSet provides endpoints for CRUD operations and additional custom actions
    related to Blog instances. It includes default actions like list, create, retrieve,
    update, and destroy, as well as a custom action for retrieving all blogs.
    """

    queryset = Blog.objects.all()
    serializer_class = BlogSerializer
    permission_classes = [
        IsAuthenticated,
        ManageBlogPermission,
    ]

    @action(
        detail=False,
        methods=["GET"],
        permission_classes=[permissions.AllowAny],
        name="get-blogs",
    )
    def get_blogs(self, request):
        """
        Custom action to retrieve all blogs.

        This action retrieves all Blog instances and serializes them using BlogSerializer.
        It is accessible to any user without authentication.

        Returns:
            Response: Serialized data containing all Blog instances.
        """
        blogs = Blog.objects.all()
        serializer = BlogSerializer(blogs, many=True)
        return Response(serializer.data)
