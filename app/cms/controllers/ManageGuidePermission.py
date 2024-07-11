"""
Module for defining custom permissions related to managing guide.

This module provides the `ManageBlogPermission` class, which extends `BasePermission`
from Django REST Framework. It checks if the authenticated user has the necessary
permissions to manage guide.

"""

from django.contrib.auth import get_user_model

from rest_framework.permissions import BasePermission


class ManageGuidePermission(BasePermission):
    """
    Custom permission class to check if the user has specific permissions to manage guide.
    """

    def has_permission(self, request, view):
        """
        Check if the authenticated user has the necessary permissions to manage guide.

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
            admin.has_permission("add_guidethematic")
            and admin.has_permission("change_guidethematic")
            and admin.has_permission("delete_guidethematic")
            and admin.has_permission("view_guidethematic")
            and admin.has_permission("add_guidearticle")
            and admin.has_permission("change_guidearticle")
            and admin.has_permission("delete_guidearticle")
            and admin.has_permission("view_guidearticle")
        )
