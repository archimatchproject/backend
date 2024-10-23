"""
Module defining the TermsAndConditionsService.

This module contains the TermsAndConditionsService class, which provides
business logic for creating TermsAndConditions instances.
"""

from django.db import transaction

from rest_framework import serializers
from rest_framework import status
from rest_framework.exceptions import APIException
from rest_framework.response import Response

from app.cms.models.TermsAndConditions import TermsAndConditions
from app.cms.serializers.TermsAndConditionsSerializer import TermsAndConditionsSerializer


class TermsAndConditionsService:
    """
    Service class for the TermsAndConditions model.

    This class provides business logic for creating TermsAndConditions instances.
    """

    @classmethod
    def create_terms_and_conditions(cls, request):
        """
        Handle the creation of a new TermsAndConditions instance.

        Args:
            request (Request): The request object.

        Returns:
            Response: The response object containing the created instance data.
        """
        serializer = TermsAndConditionsSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        validated_data = serializer.validated_data

        with transaction.atomic():
            terms = TermsAndConditions.objects.create(
                **validated_data, admin=request.user.admin
            )
            return True,TermsAndConditionsSerializer(terms).data

        