"""
Module defining the CGUCGVPolicyService.

This module contains the CGUCGVPolicyService class, which provides
business logic for creating CGU/CGV Policy instances.
"""

from django.db import transaction
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from app.cms.models.CGUCGVPolicy import CGUCGVPolicy
from app.cms.serializers.CGUCGVPolicySerializer import CGUCGVPolicySerializer
from app.users.models.Admin import Admin


class CGUCGVPolicyService:
    """
    Service class for the CGUCGVPolicy model.

    This class provides business logic for creating and managing CGU/CGV Policy instances.
    """

    @classmethod
    def create_cgucgv_policy(cls, request):
        """
        Handle the creation of a new CGUCGVPolicy instance.

        Args:
            request (Request): The request object.

        Returns:
            dict: The serialized data of the created CGUCGVPolicy instance.
        """
        serializer = CGUCGVPolicySerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        validated_data = serializer.validated_data

        with transaction.atomic():
            policy = CGUCGVPolicy.objects.create(**validated_data, admin=request.user.admin)
            return True,CGUCGVPolicySerializer(policy).data

    @classmethod
    def get_policy_by_admin(cls, request):
        """
        Retrieve the CGUCGVPolicy instance associated with the given admin.

        Args:
            admin (Admin): The admin instance.

        Returns:
            dict: The serialized data of the CGUCGVPolicy instance.

        Raises:
            NotFound: If no policy is found for the admin.
        """
        user = request.user

        admin = Admin.objects.get(user=user)
        policy = CGUCGVPolicy.objects.get(admin=admin)
        return True,CGUCGVPolicySerializer(policy).data