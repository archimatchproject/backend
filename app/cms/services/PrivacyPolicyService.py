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
        try:
            with transaction.atomic():
                policy = PrivacyPolicy.objects.create(**validated_data, admin=request.user.admin)
                return Response(
                    PrivacyPolicySerializer(policy).data, status=status.HTTP_201_CREATED
                )

        except serializers.ValidationError as e:
            raise e
        except Exception as e:
            raise APIException(detail=f"Error creating Privacy Policy: {e}")
