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
