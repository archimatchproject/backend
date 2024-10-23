"""
Module for defining custom permissions.

This module provides the `NotSuspendedPermission` class, which extends
`BasePermission` from Django REST Framework. It ensures that the authenticated
user is not suspended before granting access.
"""

from django.contrib.auth import get_user_model

from rest_framework.permissions import BasePermission


class NotSuspendedPermission(BasePermission):
    """
    Custom permission class to check if the authenticated user is not suspended.

    This permission class grants access only if the user is not suspended.
    It can be used to restrict access to certain views based on the user's
    suspended status.
    """

    def has_permission(self, request, view):
        """
        Check if the authenticated user is not suspended and thus has permission
        to access the requested resource.

        Args:
            request (HttpRequest): The request object containing the user's information.
            view (APIView): The view requesting the permission check.

        Returns:
            bool: True if the user is not suspended and thus has permission; False otherwise.
        """

        User = get_user_model()
        try:
            user = User.objects.get(pk=request.user.pk)
        except User.DoesNotExist:
            return False

        return not user.is_suspended
