from django.contrib.auth import get_user_model

from rest_framework.permissions import BasePermission


class ManageBlogPermission(BasePermission):
    def has_permission(self, request, view):

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
