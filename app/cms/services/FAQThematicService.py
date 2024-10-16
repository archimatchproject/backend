"""
Module defining the FAQThematicService.

This module contains the FAQThematicService class, which provides
business logic for creating and updating FAQThematic instances
along with their related FAQQuestion instances.

Classes:
    FAQThematicService: Service class for FAQThematic operations.
"""

from django.db import transaction

from rest_framework import serializers
from rest_framework import status
from rest_framework.exceptions import APIException
from rest_framework.response import Response

from app.cms.models.FAQThematic import FAQThematic
from app.cms.serializers.FAQThematicSerializer import FAQThematicSerializer


class FAQThematicService:
    """
    Service class for the FAQThematic model.

    This class provides business logic for creating and updating FAQThematic instances
    along with their related FAQQuestion instances.

    Methods:
        create_faq_thematic(data): Handles validation and creation of a new FAQThematic.
        update_faq_thematic(instance, data): Handles validation and updating of an existing
        FAQThematic.
    """

    @classmethod
    def create_faq_thematic(cls, request):
        """
        Handle the creation of a new FAQThematic instance along with related FAQQuestion instances.

        Args:
            data (dict): The validated data for creating an FAQThematic.

        Returns:
            Response: The response object containing the created instance data.
        """
        serializer = FAQThematicSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        validated_data = serializer.validated_data
        target_user_type = request.data.get("targetUserType",False)
        if not target_user_type:
            raise serializers.ValidationError(detail="target user type is required")

        with transaction.atomic():

            thematic = FAQThematic.objects.create(**validated_data,target_user_type=target_user_type, admin=request.user.admin)
            return True,FAQThematicSerializer(thematic).data
        
    @classmethod
    def update_faq_thematic(cls, instance, request):
        """
        Handle the update of an existing FAQThematic instance along with related
        FAQQuestion instances.

        Args:
            instance (FAQThematic): The existing FAQThematic instance.
            data (dict): The validated data for updating an FAQThematic.

        Returns:
            Response: The response object containing the updated instance data.
        """
        serializer = FAQThematicSerializer(instance, data=request.data)
        serializer.is_valid(raise_exception=True)
        validated_data = serializer.validated_data

        with transaction.atomic():
            instance.title = validated_data.get("title", instance.title)
            instance.save()
            return True,FAQThematicSerializer(instance).data
        