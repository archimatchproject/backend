"""
Module: announcement Service

This module defines the AnnouncementService class that handles announcement-related operations .

Classes:
    AnnouncementService: Service class for announcement-related operations.

"""


from rest_framework.exceptions import APIException

from app.selection.models.Selection import Selection
from app.selection.serializers.SelectionSerializer import SelectionSerializer,SelectionPostSerializer
from app.users.models.Architect import Architect
from django.core.exceptions import ValidationError
from rest_framework import serializers

class SelectionService:
    """
    Service class for handling announcement-related operations .

    """

    @classmethod
    def create_selection(cls, data,user):
        """
        Creates a Selection for a given announcement and the architect.

        Args:
            announcement (Announcement): The announcement instance.
            architect (Architect): The architect instance.

        Returns:
            Selection: The created Selection instance.

        Raises:
            APIException: If there are issues creating the selection.
        """
        try:
            
            
            architect = Architect.objects.get(user=user)
            data["architect"] = architect.id
            serializer = SelectionPostSerializer(data=data)
            serializer.is_valid(raise_exception=True)
            validated_data = serializer.validated_data
            announcement = validated_data.get('announcement')
            architect = validated_data.get("architect")

            # Ensure no more than 4 selections for the announcement
            if Selection.objects.filter(announcement=announcement).count() >= 4:
                raise APIException("Maximum of 4 selections reached for this announcement.")

            # Ensure only one accepted selection if status is 'accepted'
            if Selection.objects.filter(announcement=announcement, status='accepted').exists():
                raise APIException("Another architect has already been accepted for this announcement.")

            if architect.subscription_plan.remaining_tokens < 5 :
                raise APIException("you don't have the required token for this announcement")
            
            # Create and save the new selection
            selection = Selection.objects.create(
                announcement=announcement,
                architect=architect,
            )
            subscription_plan = architect.subscription_plan
            subscription_plan.remaining_tokens -= 5
            subscription_plan.save()

            return selection
        
        except serializers.ValidationError as e:
            raise e
