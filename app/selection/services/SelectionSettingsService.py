"""
Module: Selection Settings Service

This module defines the `SelectionSettingsService` class that handles operations
related to `SelectionSettings`, such as retrieving and updating the selection settings.

Classes:
    SelectionSettingsService: Service class for `SelectionSettings` operations.
"""

from django.db import transaction

from rest_framework.exceptions import APIException
from rest_framework.exceptions import ValidationError

from app.selection import DAYS_AFTER_CALL_EMAIL_CHOICES
from app.selection import DAYS_BEFORE_CALL_EMAIL_CHOICES
from app.selection import DAYS_FOR_ADMIN_MANAGEMENT_CHOICES
from app.selection import DAYS_TO_LOCK_PROJECT_CHOICES
from app.selection import DAYS_TO_PHONE_CALL_CHOICES
from app.selection import DAYS_TO_REDIFFUSE_CHOICES
from app.selection import PHASE_DAYS_CHOICES
from app.selection import TIMES_TO_UNLOCK_PROJECT_CHOICES
from app.selection.models.SelectionSettings import SelectionSettings
from app.selection.serializers.SelectionSettingsSerializer import SelectionSettingsSerializer


class SelectionSettingsService:
    """
    Service class for handling operations related to `SelectionSettings`.

    Provides methods to retrieve and update the selection settings.
    """

    @classmethod
    def get_selection_settings(cls, request, pk):
        """
        Retrieve the selection settings.

        Args:
            request (HttpRequest): The HTTP request object.

        Returns:
            tuple: A tuple containing a success flag (bool) and the serialized selection settings
            data (dict).

        Raises:
            APIException: If no `SelectionSettings` instance exists.
        """
        settings = SelectionSettings.objects.get(id=pk)
        if not settings:
            raise APIException("Selection settings not configured.")

        serializer = SelectionSettingsSerializer(settings)
        return True, serializer.data

    @classmethod
    @transaction.atomic
    def update_selection_settings(cls, data, pk):
        """
        Update a specific selection setting.

        Args:
            data (dict): A dictionary containing the field name (`name`) and its updated value
            (`value`).
            pk (int): The primary key of the SelectionSettings instance to update.

        Returns:
            tuple: A tuple containing a success flag (bool) and the updated serialized selection
            settings data (dict).

        Raises:
            ValidationError: If validation fails for the updated field.
            APIException: If no `SelectionSettings` instance exists or the field name is invalid.
        """

        try:
            settings = SelectionSettings.objects.get(id=pk)
        except SelectionSettings.DoesNotExist:
            raise APIException("Selection settings not configured.")

        field_name = data.get("name")

        new_value = data.get("value")

        if not hasattr(settings, field_name):
            raise ValidationError(detail=f"Field '{field_name}' does not exist in SelectionSettings.")

        # Dynamically update the field value
        setattr(settings, field_name, new_value)

        # Validate the model before saving
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
            tuple: A tuple containing a success flag (bool) and the serialized selection settings
            data (dict).

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
        return True, data
