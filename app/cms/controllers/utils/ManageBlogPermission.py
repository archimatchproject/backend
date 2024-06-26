"""
Module for defining custom permissions related to managing blogs.

This module provides the `ManageBlogPermission` class, which extends `BasePermission`
from Django REST Framework. It checks if the authenticated user has the necessary
permissions to manage blogs.

"""

from django.contrib.auth import get_user_model

from rest_framework.permissions import BasePermission


class ManageBlogPermission(BasePermission):
    """
    Custom permission class to check if the user has specific permissions to manage blogs.
    """

    def has_permission(self, request, view):
        """
        Check if the authenticated user has the necessary permissions to manage blogs.

        Args:
            request (HttpRequest): The request object.
            view (APIView): The view requesting permission check.

        Returns:
            bool: True if the user has permission, False otherwise.
        """
        User = get_user_model()
        try:
            admin = User.objects.get(pk=request.user.pk).admin
        except User.DoesNotExist:
            return False

        if admin.super_user:
            return True

        return (
            admin.has_permission("add_blog")
            and admin.has_permission("change_blog")
            and admin.has_permission("delete_blog")
            and admin.has_permission("view_blog")
        )
