"""
Module for defining custom permissions related to managing reporting.

This module provides the `ManageReportingPermission` class, which extends `BasePermission`
from Django REST Framework. It checks if the authenticated user has the necessary
permissions to manage reporting.

"""

from django.contrib.auth import get_user_model

from rest_framework.permissions import BasePermission
from rest_framework.serializers import ValidationError


class ManageReportingPermission(BasePermission):
    """
    Custom permission class to check if the user has specific permissions to manage reporting.
    """

    def has_permission(self, request, view):
        """
        Check if the authenticated user has the necessary permissions to manage reporting.

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
            admin.has_permission("add_architectreport")
            and admin.has_permission("change_architectreport")
            and admin.has_permission("delete_architectreport")
            and admin.has_permission("view_architectreport")
            and admin.has_permission("add_projectreport")
            and admin.has_permission("change_projectreport")
            and admin.has_permission("delete_projectreport")
            and admin.has_permission("view_projectreport")
            and admin.has_permission("add_reviewreport")
            and admin.has_permission("change_reviewreport")
            and admin.has_permission("delete_reviewreport")
            and admin.has_permission("view_reviewreport")
        )
