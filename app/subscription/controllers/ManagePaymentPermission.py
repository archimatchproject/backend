"""
Module for defining custom permissions related to managing payment.

This module provides the `ManageBlogPermission` class, which extends `BasePermission`
from Django REST Framework. It checks if the authenticated user has the necessary
permissions to manage payment.

"""

from django.contrib.auth import get_user_model

from rest_framework.permissions import BasePermission
from rest_framework.serializers import ValidationError


class ManagePaymentPermission(BasePermission):
    """
    Custom permission class to check if the user has specific permissions to manage payment.
    """

    def has_permission(self, request, view):
        """
        Check if the authenticated user has the necessary permissions to manage payment.

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
        except Exception:
            raise ValidationError(detail="Authenticated user is not an Admin.")
        if admin.super_user:
            return True

        return (
            admin.has_permission("add_payment")
            and admin.has_permission("change_payment")
            and admin.has_permission("delete_payment")
            and admin.has_permission("view_payment")
        )
