"""
Module defining the PrivacyPolicyService.

This module contains the PrivacyPolicyService class, which provides
business logic for creating PrivacyPolicy instances.
"""

from django.db import transaction

from rest_framework import serializers
from rest_framework import status
from rest_framework.exceptions import APIException
from rest_framework.response import Response

from app.cms.models.PrivacyPolicy import PrivacyPolicy
from app.cms.serializers.PrivacyPolicySerializer import PrivacyPolicySerializer
from app.users.models.Admin import Admin


class PrivacyPolicyService:
    """
    Service class for the PrivacyPolicy model.

    This class provides business logic for creating PrivacyPolicy instances.
    """

    @classmethod
    def create_privacy_policy(cls, request):
        """
        Handle the creation of a new PrivacyPolicy instance.

        Args:
            request (Request): The request object.

        Returns:
            Response: The response object containing the created instance data.
        """
        serializer = PrivacyPolicySerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        validated_data = serializer.validated_data

        with transaction.atomic():
            policy = PrivacyPolicy.objects.create(**validated_data, admin=request.user.admin)
            return True,PrivacyPolicySerializer(policy).data
        
    @classmethod
    def get_policy_by_admin(cls, request):
        """
        Retrieve the PrivacyPolicy instance associated with the given admin.

        Args:
            admin (Admin): The admin instance.

        Returns:
            dict: The serialized data of the PrivacyPolicy instance.

        Raises:
            NotFound: If no policy is found for the admin.
        """
        user = request.user

        admin = Admin.objects.get(user=user)
        policy = PrivacyPolicy.objects.get(admin=admin)
        return True,PrivacyPolicySerializer(policy).data