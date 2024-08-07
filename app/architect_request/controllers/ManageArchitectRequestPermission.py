"""
Module for defining custom permissions related to managing architect requests.

This module provides the `ManageArchitectRequestPermission` class, which extends
`BasePermission`
from Django REST Framework. It checks if the authenticated user has the necessary
permissions to manage architect requests.

"""

from django.contrib.auth import get_user_model

from rest_framework.permissions import BasePermission


class ManageArchitectRequestPermission(BasePermission):
    """
    Custom permission class to check if the user has specific permissions to manage
    architect requests.
    """

    def has_permission(self, request, view):
        """
        Check if the authenticated user has the necessary permissions to manage
        architect requests.

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
            admin.has_permission("add_architectrequest")
            and admin.has_permission("change_architectrequest")
            and admin.has_permission("delete_architectrequest")
            and admin.has_permission("view_architectrequest")
        )
