from rest_framework.permissions import BasePermission

class IsSuperUser(BasePermission):
    """
    Allows access only to super users.
    """
    def has_permission(self, request, view):
        # Check if the user is authenticated and a super user
        return request.user and request.user.is_authenticated and hasattr(request.user, 'admin') and request.user.admin.super_user
