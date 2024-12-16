"""
Module: announcement Service

This module defines the AnnouncementService class that handles announcement-related operations .

Classes:
    AnnouncementService: Service class for announcement-related operations.

"""


from rest_framework.exceptions import APIException
from django.utils import timezone
from app.announcement.filters.AnnouncementFilter import AnnouncementFilter
from app.announcement.models.Announcement import Announcement
from app.announcement.serializers.AnnouncementSerializer import AnnouncementOutputSerializer, AnnouncementSerializer
from app.core.pagination import CustomPagination
from app.selection.filters import SelectionFilter
from app.selection.models.ActionLog import ActionLog
from app.selection.models.Phase import Phase
from app.selection.models.Selection import Selection
from app.selection.models.SelectionSettings import SelectionSettings
from app.selection.serializers.ActionLogSerializer import ActionLogSerializer
from app.selection.serializers.SelectionSerializer import SelectionSerializer,SelectionPostSerializer
from app.users.models.Admin import Admin
from app.users.models.Architect import Architect
from django.core.exceptions import ValidationError
from rest_framework import serializers
from datetime import datetime, timedelta
from app.selection import BLOCK_PROJECT, CANCEL_PROJECT, CHANGE_DEADLINE, CONFIRM_DISCUSSION_PHASE, DECISION, DISCUSSION, NOT_SELECTED, QUOTES, REBROADCAST_PROJECT
from django.db import transaction
from rest_framework.response import Response
from rest_framework import status
from django.utils.timezone import now


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
        phase_settings = cls.get_selection_settings(name=DISCUSSION)
        phase_duration_days = phase_settings.phase_days
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

        return True, SelectionSerializer(selection,context={}).data



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
        return True,SelectionSerializer(selections, many=True,context={}).data
    
    
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
            serialized_selections = SelectionSerializer(page, many=True,context={}).data
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

        phase_settings = cls.get_selection_settings(name=QUOTES)
        phase_duration_days = phase_settings.phase_days
        
        phase.number = 2
        phase.name = QUOTES
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

        serializer = SelectionSerializer(queryset, many=True,context={})
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
    
    @classmethod
    def get_not_selected_announcements(self, request):
        """
        Handle GET request and return paginated not selected announcements objects.

        This method retrieves all not selected announcements objects from the database, applies
        pagination based on the parameters in the request, and returns the paginated
        results. If the pagination is not applied correctly, it returns a 400 Bad Request response.

        Args:
            request (HttpRequest): The incoming HTTP request.

        Returns:
            Response: A paginated response containing not selected announcements objects or an error message.
        """

        selection_settings = self.get_selection_settings(name=NOT_SELECTED)
        phase_days = selection_settings.phase_days
        
        phase_days = selection_settings.phase_days
        days_before = now().date() + timedelta(days=selection_settings.days_for_admin_display)
        announcements = Announcement.objects.filter(
            selections__isnull=True,
            suggested_at__lte=days_before - timedelta(days=phase_days),
        ).order_by("created_at")

        filtered_queryset = AnnouncementFilter(request.GET, queryset=announcements).qs
        paginator = self.pagination_class()
        page = paginator.paginate_queryset(filtered_queryset, request)
        if page is not None:
            serializer = AnnouncementOutputSerializer(page, many=True)
            return paginator.get_paginated_response(serializer.data)
        
        return Response({"message": "error retrieving data"}, status=status.HTTP_400_BAD_REQUEST)
    
    @classmethod
    def get_selection_settings(cls,name:str):
        """
        Utility function to retrieve the SelectionSettings singleton instance.

        Returns:
            SelectionSettings: The instance of the SelectionSettings model.

        Raises:
            ValidationError: If SelectionSettings is not configured.
        """
        selection_settings = SelectionSettings.objects.filter(name=name).first()
        if not selection_settings:
            raise ValidationError(detail="Selection settings not configured.")
        return selection_settings
    
    
    @classmethod
    @transaction.atomic
    def broadcast_announcement(cls, announcement_id):
        """
        broadcast announcement

        Args:
            announcement_id (int): The ID of the announcement to update.

        Returns:
            tuple: (bool, str) A success flag and a success message.

        """
        
        announcement = Announcement.objects.select_for_update().get(id=announcement_id)
        announcement.is_broadcasted = True
        announcement.save()

        return True, "the broadcast of the announcement is successfull"
    
    
    @classmethod
    def get_discussion_phase_selections(self, request):
        """
        Handle GET request and return paginated not selected announcements objects.

        This method retrieves all not selected announcements objects that are in the
        'DISCUSSION' phase and have 3, 2, 1, or 0 days left until the limit date. Pagination is applied
        based on the parameters in the request.

        Args:
            request (HttpRequest): The incoming HTTP request.

        Returns:
            Response: A paginated response containing the filtered selections or an error message.
        """

        selection_settings = self.get_selection_settings(name=DISCUSSION)
        today = now().date()
        selections = Selection.objects.filter(
            phase__name=DISCUSSION,
             phase__limit_date__lte=today + timedelta(days=selection_settings.days_for_admin_display)
        ).order_by("phase__start_date")
        
        paginator = self.pagination_class()
        page = paginator.paginate_queryset(selections, request)
        if page is not None:
            serializer = SelectionSerializer(page, many=True,context={'selection_settings': selection_settings})
            return paginator.get_paginated_response(serializer.data)
        
        return Response({"message": "error retrieving data"}, status=status.HTTP_400_BAD_REQUEST)
    
    
    @classmethod
    def get_selection_logs(cls,selection_id):
        """
        Retrieve the action logs associated with a specific selection ID.

        This method filters the ActionLog entries based on the `selection_id` 
        stored in the `details` JSON field and orders them by the most recent logs.

        Args:
            selection_id (int): The ID of the selection for which to fetch action logs.

        Returns:
            tuple: A tuple containing:
                - bool: `True` if logs are found.
                - list: A serialized list of action logs.

        Raises:
            APIException: If no logs are found for the given selection ID.
        """
        logs = ActionLog.objects.filter(details__selection_id=selection_id).order_by('-timestamp')

        if not logs.exists():
            raise APIException(detail="No logs found for this selection.")
        serializer = ActionLogSerializer(logs, many=True)
        return True,serializer.data
    
    
    @classmethod
    @transaction.atomic
    def broadcast_selection_announcement(cls, selection_id,user):
        """
        broadcast announcement for a particular selection

        Args:
            selection_id (int): The ID of the selection to update.

        Returns:
            tuple: (bool, str) A success flag and a success message.

        """
        admin = Admin.objects.get(user=user)
        selection = Selection.objects.select_for_update().get(id=selection_id)
        announcement = selection.announcement
        announcement.is_broadcasted = True
        announcement.save()
        selection.save()
        
        ActionLog.objects.create(
            admin=admin,
            action=REBROADCAST_PROJECT,
            details={"selection_id": selection_id}
        )

        return True, "the broadcast of the announcement is successfull"
    
    @classmethod
    @transaction.atomic
    def block_selection(cls, selection_id,user):
        """
        block selection for a particular architect

        Args:
            selection_id (int): The ID of the selection to update.

        Returns:
            tuple: (bool, str) A success flag and a success message.

        """
        admin = Admin.objects.get(user=user)
        selection = Selection.objects.select_for_update().get(id=selection_id)
        selection.is_blocked = True
        selection.save()
        
        ActionLog.objects.create(
            admin=admin,
            action=BLOCK_PROJECT,
            details={"selection_id": selection_id}
        )

        return True, "the broadcast of the announcement is successfull"
    
    
    @classmethod
    @transaction.atomic
    def change_selection_deadline(cls, selection_id,user,data):
        """
        block selection for a particular architect

        Args:
            selection_id (int): The ID of the selection to update.

        Returns:
            tuple: (bool, str) A success flag and a success message.

        """
        days_number = data.get("days_number",None)
        if days_number is None:
            raise APIException(detail="number of days has to be defined")
        admin = Admin.objects.get(user=user)
        selection = Selection.objects.select_for_update().get(id=selection_id)
        print(selection.phase)
        phase = selection.phase 
        phase.limit_date += timedelta(days=days_number) 
        phase.save()
        selection.save()
        
        ActionLog.objects.create(
            admin=admin,
            action=CHANGE_DEADLINE,
            details={"selection_id": selection_id}
        )

        return True, "the broadcast of the announcement is successfull"
    
    @classmethod
    @transaction.atomic
    def confirm_discussion_phase_admin(cls, selection_id,user):
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
        
        stat,message= cls.confirm_discussion_phase(selection_id=selection_id)
        admin = Admin.objects.get(user=user)
        ActionLog.objects.create(
            admin=admin,
            action=CONFIRM_DISCUSSION_PHASE,
            details={"selection_id": selection_id}
        )
        return stat, message
    
    
    @classmethod
    @transaction.atomic
    def cancel_selection(cls, selection_id,user):
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

        phase_settings = cls.get_selection_settings(name=QUOTES)
        phase_duration_days = phase_settings.phase_days
        
        phase.number = 3
        phase.name = DECISION
        phase.start_date = timezone.now()

        phase.limit_date = phase.start_date + timezone.timedelta(days=phase_duration_days)
        
        phase.save()
        admin = Admin.objects.get(user=user)
        ActionLog.objects.create(
            admin=admin,
            action=CANCEL_PROJECT,
            details={"selection_id": selection_id}
        )
        return True, "Project canceled"