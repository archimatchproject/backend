"""
Module defining the FAQQuestionService.

This module contains the FAQQuestionService class, which provides
business logic for creating and updating FAQQuestion instances
along with their related FAQQuestion instances.

Classes:
    FAQQuestionService: Service class for FAQQuestion operations.
"""

from django.db import transaction

from rest_framework import serializers
from rest_framework import status
from rest_framework.exceptions import APIException
from rest_framework.response import Response

from app.cms.models.FAQQuestion import FAQQuestion
from app.cms.serializers.FAQQuestionSerializer import FAQQuestionSerializer


class FAQQuestionService:
    """
    Service class for the FAQQuestion model.

    This class provides business logic for creating and updating FAQQuestion instances
    along with their related FAQQuestion instances.

    Methods:
        create_faq_question(data): Handles validation and creation of a new FAQQuestion.
        update_faq_question(instance, data): Handles validation and updating of an existing
        FAQQuestion.
    """

    @classmethod
    def create_faq_question(cls, request):
        """
        Handle the creation of a new FAQQuestion instance along with related FAQQuestion instances.

        Args:
            data (dict): The validated data for creating an FAQQuestion.

        Returns:
            Response: The response object containing the created instance data.
        """
        serializer = FAQQuestionSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        validated_data = serializer.validated_data
        with transaction.atomic():

            question = FAQQuestion.objects.create(**validated_data, admin=request.user.admin)
            return True,FAQQuestionSerializer(question).data
        

    @classmethod
    def update_faq_question(cls, instance, request):
        """
        Handle the update of an existing FAQQuestion instance along with related
        FAQQuestion instances.

        Args:
            instance (FAQQuestion): The existing FAQQuestion instance.
            data (dict): The validated data for updating an FAQQuestion.

        Returns:
            Response: The response object containing the updated instance data.
        """
        serializer = FAQQuestionSerializer(instance, data=request.data)
        serializer.is_valid(raise_exception=True)
        validated_data = serializer.validated_data

        with transaction.atomic():
            fields = ["question", "response", "faq_thematic", "guide_thematic", "guide_article"]
            for field in fields:
                setattr(instance, field, validated_data.get(field, getattr(instance, field)))

            instance.save()

            return True,FAQQuestionSerializer(instance).data

        