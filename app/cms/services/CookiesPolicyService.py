"""
Module defining the CookiesPolicyService.

This module contains the CookiesPolicyService class, which provides
business logic for creating CookiesPolicy instances.
"""

from django.db import transaction

from app.cms.models.CookiesPolicy import CookiesPolicy
from app.cms.serializers.CookiesPolicySerializer import CookiesPolicySerializer
from app.users.models.Admin import Admin


class CookiesPolicyService:
    """
    Service class for the CookiesPolicy model.

    This class provides business logic for creating CookiesPolicy instances.
    """

    @classmethod
    def create_cookies_policy(cls, request):
        """
        Handle the creation of a new CookiesPolicy instance.

        Args:
            request (Request): The request object.

        Returns:
            Response: The response object containing the created instance data.
        """
        serializer = CookiesPolicySerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        validated_data = serializer.validated_data

        with transaction.atomic():
            policy = CookiesPolicy.objects.create(**validated_data, admin=request.user.admin)
            return True, CookiesPolicySerializer(policy).data

    @classmethod
    def get_policy_by_admin(cls, request):
        """
        Retrieve the CookiesPolicy instance associated with the given admin.

        Args:
            admin (Admin): The admin instance.

        Returns:
            dict: The serialized data of the CookiesPolicy instance.

        Raises:
            NotFound: If no policy is found for the admin.
        """
        user = request.user

        admin = Admin.objects.get(user=user)
        policy = CookiesPolicy.objects.get(admin=admin)
        return True,CookiesPolicySerializer(policy).data
        