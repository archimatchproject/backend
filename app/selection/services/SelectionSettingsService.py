"""
Module: Selection Settings Service

This module defines the `SelectionSettingsService` class that handles operations 
related to `SelectionSettings`, such as retrieving and updating the selection settings.

Classes:
    SelectionSettingsService: Service class for `SelectionSettings` operations.
"""

from rest_framework.exceptions import APIException
from django.db import transaction
from app.selection.models.SelectionSettings import SelectionSettings
from app.selection.serializers.SelectionSettingsSerializer import SelectionSettingsSerializer
from app.selection import (
    PHASE_DAYS_CHOICES,
    DAYS_BEFORE_CALL_EMAIL_CHOICES,
    DAYS_TO_PHONE_CALL_CHOICES,
    DAYS_AFTER_CALL_EMAIL_CHOICES,
    DAYS_TO_REDIFFUSE_CHOICES,
    DAYS_TO_LOCK_PROJECT_CHOICES,
    TIMES_TO_UNLOCK_PROJECT_CHOICES,
    DAYS_FOR_ADMIN_MANAGEMENT_CHOICES,
)

class SelectionSettingsService:
    """
    Service class for handling operations related to `SelectionSettings`.

    Provides methods to retrieve and update the selection settings.
    """

    @classmethod
    def get_selection_settings(cls, request):
        """
        Retrieve the selection settings.

        Args:
            request (HttpRequest): The HTTP request object.

        Returns:
            tuple: A tuple containing a success flag (bool) and the serialized selection settings data (dict).

        Raises:
            APIException: If no `SelectionSettings` instance exists.
        """
        settings = SelectionSettings.objects.first()
        if not settings:
            raise APIException("Selection settings not configured.")
        
        serializer = SelectionSettingsSerializer(settings)
        return True, serializer.data

    @classmethod
    @transaction.atomic
    def update_selection_settings(cls, data):
        """
        Update the selection settings.

        Args:
            data (dict): A dictionary containing the updated selection settings values.

        Returns:
            tuple: A tuple containing a success flag (bool) and the updated serialized selection settings data (dict).

        Raises:
            ValidationError: If validation fails for any of the updated settings fields.
            APIException: If no `SelectionSettings` instance exists to update.
        """
        settings = SelectionSettings.objects.first()
        if not settings:
            raise APIException("Selection settings not configured.")
        

        for key, value in data.items():
            if hasattr(settings, key):
                setattr(settings, key, value)

  
        settings.full_clean()
        settings.save()

        serializer = SelectionSettingsSerializer(settings)
        return True, serializer.data

    
    @classmethod
    def get_selection_settings_choices(cls, request):
        """
        Retrieve the selection settings choices.

        Args:
            request (HttpRequest): The HTTP request object.

        Returns:
            tuple: A tuple containing a success flag (bool) and the serialized selection settings data (dict).

        Raises:
            APIException: If no `SelectionSettings` instance exists.
        """
        data = {
            "phase_days": PHASE_DAYS_CHOICES,
            "days_before_call_email": DAYS_BEFORE_CALL_EMAIL_CHOICES,
            "days_to_phone_call": DAYS_TO_PHONE_CALL_CHOICES,
            "days_after_call_email": DAYS_AFTER_CALL_EMAIL_CHOICES,
            "days_to_rediffuse": DAYS_TO_REDIFFUSE_CHOICES,
            "days_to_lock_project": DAYS_TO_LOCK_PROJECT_CHOICES,
            "times_to_unlock_project": TIMES_TO_UNLOCK_PROJECT_CHOICES,
            "days_for_admin_management": DAYS_FOR_ADMIN_MANAGEMENT_CHOICES,
        }
        return True,data