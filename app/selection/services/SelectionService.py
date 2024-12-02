"""
Module: announcement Service

This module defines the AnnouncementService class that handles announcement-related operations .

Classes:
    AnnouncementService: Service class for announcement-related operations.

"""


from rest_framework.exceptions import APIException
from django.utils import timezone
from app.announcement.models.Announcement import Announcement
from app.core.pagination import CustomPagination
from app.selection.filters import SelectionFilter
from app.selection.models.Phase import Phase
from app.selection.models.Selection import Selection
from app.selection.models.SelectionSettings import SelectionSettings
from app.selection.serializers.SelectionSerializer import SelectionSerializer,SelectionPostSerializer
from app.users.models.Architect import Architect
from django.core.exceptions import ValidationError
from rest_framework import serializers
from datetime import datetime, timedelta
from app.selection import DISCUSSION
from django.db import transaction
from rest_framework.response import Response
from rest_framework import status

class SelectionService:
    """
    Service class for handling announcement-related operations .

    """
    
    pagination_class = CustomPagination
    
    @classmethod
    def create_selection(cls, data, user):
        """
        Creates a Selection for a given announcement and the architect.

        Args:
            data (dict): The data for creating the selection.
            user (User): The user making the selection (who is an architect).

        Returns:
            tuple: (bool, dict) indicating success and the serialized selection data.

        Raises:
            APIException: If there are issues creating the selection.
        """
        # Get the architect from the user
        architect = Architect.objects.get(user=user)
        data["architect"] = architect.id

        # Validate the selection data
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

        # Ensure the architect has enough tokens
        if architect.subscription_plan.remaining_tokens < 5:
            raise APIException("You don't have the required tokens for this announcement.")

        # Create and save the new selection
        selection = Selection.objects.create(
            announcement=announcement,
            architect=architect,
        )

        # Deduct 5 tokens from the architect's subscription plan
        subscription_plan = architect.subscription_plan
        if (subscription_plan.remaining_tokens <=0):
            raise APIException("You don't have enough tokens.")
        
        if announcement.token_number is not None:
            subscription_plan.remaining_tokens -= announcement.token_number
        else:
            subscription_plan.remaining_tokens -= 5
        
        subscription_plan.save()

        # Fetch the number of days for the phase from the SelectionSettings model
        phase_duration_days = cls.get_phase_duration_from_settings()

        # Create the Phase
        start_date = datetime.now().date()
        limit_date = start_date + timedelta(days=phase_duration_days)

        phase = Phase.objects.create(
            name=DISCUSSION,
            number=1,
            start_date=start_date,
            limit_date=limit_date,
        )

        # Assign the created phase to the selection
        selection.phase = phase
        selection.save()

        return True, SelectionSerializer(selection).data

    @staticmethod
    def get_phase_duration_from_settings():
        """
        Fetch the phase duration from the SelectionSettings model.
        
        Returns:
            int: The number of days for the phase duration.

        Raises:
            APIException: If the setting is not found or invalid.
        """

        settings = SelectionSettings.objects.first()
        if not settings or settings.phase_days is None:
            raise APIException("Phase duration settings are not properly configured.")
        
        return settings.phase_days

    @classmethod
    def get_announcement_selections(cls, announcement_id):
        """
        Retrieves selections associated with the given announcement.

        Args:
            announcement_id (int): The ID of the announcement.

        Returns:
            list: A list of serialized selections for the given announcement.
        
        Raises:
            APIException: If there are no selections for the announcement.
        """
        selections = Selection.objects.filter(announcement_id=announcement_id)
        
        if not selections.exists():
            raise APIException("No selections found for this announcement.")
        
        # Serialize the selections
        return True,SelectionSerializer(selections, many=True).data
    
    
    @classmethod
    def get_selections_by_architect(cls, request):
        """
        Retrieves all selections made by the given architect.

        Args:
            architect (Architect): The architect for whom selections are to be retrieved.

        Returns:
            tuple: (bool, list) indicating success and the serialized selection data.
        """
        architect = Architect.objects.get(user=request.user)
        # Retrieve selections for the given architect
        selections = Selection.objects.filter(architect=architect)
        paginator = cls.pagination_class()
        page = paginator.paginate_queryset(selections, request)
        if page is not None:
            serialized_selections = SelectionSerializer(page, many=True).data
            return paginator.get_paginated_response(serialized_selections)
        return Response([], status=status.HTTP_200_OK)
        
    
    @classmethod
    def update_selection_name(cls, selection_id, name):
        """
        Updates the name of a specific selection.

        Args:
            selection_id (int): The ID of the selection to update.
            name (str): The new name for the selection.

        Returns:
            dict: The updated selection data.

        Raises:
            APIException: If the selection is not found or any error occurs during the update.
        """
        # Find the selection by its ID
        selection = Selection.objects.get(id=selection_id)

        # Update the name of the selection
        selection.name = name
        selection.save()

        # Return the updated selection data
        return True, {"id": selection.id, "name": selection.name, "status": selection.status}

    @classmethod
    @transaction.atomic
    def confirm_discussion_phase(cls, selection_id):
        """
        Confirms the completion of the discussion phase and progresses to phase 2.

        - Updates the phase to 2.
        - Sets the start date to the current time.
        - Sets the limit date based on the number of days defined in `SelectionSettings`.

        Args:
            selection_id (int): The ID of the selection to update.

        Returns:
            tuple: (bool, dict) A success flag and the updated selection and phase data.

        Raises:
            APIException: If the selection or its phase is not found, or if there is an issue.
        """
        
        selection = Selection.objects.select_for_update().get(id=selection_id)
 
        if not selection.phase:
            raise APIException(detail="Phase not associated with the selection.")
        
        phase = selection.phase

        phase_duration_days = cls.get_phase_duration_from_settings()
        
        
        phase.number = 2
        phase.start_date = timezone.now()

        phase.limit_date = phase.start_date + timezone.timedelta(days=phase_duration_days)
        
        phase.save()

        return True, "discussion phase is confirmed"
    
    
    @classmethod
    def get_selections(cls, request):
        """
        Handle GET request and return paginated Announcement objects.

        This method retrieves all Announcement objects from the database, applies
        pagination based on the parameters in the request, and returns the paginated
        results. If the pagination is not applied correctly, it returns a 400 Bad Request response.

        Args:
            request (HttpRequest): The incoming HTTP request.

        Returns:
            Response: A paginated response containing Announcement objects or an error message.
        """
        queryset = Selection.objects.all().order_by("created_at")
        filtered_queryset = SelectionFilter(request.GET, queryset=queryset).qs
        paginator = cls.pagination_class()
        page = paginator.paginate_queryset(filtered_queryset, request)
        if page is not None:
            serializer = SelectionSerializer(page, many=True)
            return paginator.get_paginated_response(serializer.data)

        serializer = SelectionSerializer(queryset, many=True)
        return Response({"message": "error retrieving data"}, status=status.HTTP_400_BAD_REQUEST)
    
    
    @classmethod
    @transaction.atomic
    def abandon_selection(cls, selection_id):
        """
        give the hand to an architect to abandon a selection

        Args:
            selection_id (int): The ID of the selection to update.

        Returns:
            tuple: (bool, str) A success flag and a success message.

        Raises:
            APIException: If the selection or its phase is not found, or if there is an issue.
        """
        
        selection = Selection.objects.select_for_update().get(id=selection_id)
        selection.is_abandoned = True
        selection.save()

        return True, "discussion phase is confirmed"
    