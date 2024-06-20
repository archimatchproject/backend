"""
Module: app.permissions

Class: IsSuperUser

"""
from rest_framework.permissions import BasePermission


class IsSuperUser(BasePermission):
    """
    Allows access only to super users.
    """

    def has_permission(self, request, view):
        """
        Check if the user is authenticated and a super user.

        Args:
            self: Instance of the IsSuperUser class.
            request: HTTP request object.
            view: Django view object being accessed.

        Returns:
            bool: True if the user is authenticated and a super user, False otherwise.
        """
        return (
            request.user
            and request.user.is_authenticated
            and hasattr(request.user, "admin")
            and request.user.admin.super_user
        )
