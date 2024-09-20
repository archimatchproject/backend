"""
Module defining the CookiesPolicyService.

This module contains the CookiesPolicyService class, which provides
business logic for creating CookiesPolicy instances.
"""

from django.db import transaction

from app.cms.models.CookiesPolicy import CookiesPolicy
from app.cms.serializers.CookiesPolicySerializer import CookiesPolicySerializer


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
