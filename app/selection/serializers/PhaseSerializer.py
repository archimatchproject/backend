"""
This module contains the PhaseSerializer class, which is responsible for
serializing and deserializing Phase model instances.

The PhaseSerializer converts Phase objects into JSON format for API
responses and calculates the 'progress' field, which represents the
percentage of time passed between the 'start_date' and 'limit_date' of
each phase.

Key Components:
- PhaseSerializer: Extends ModelSerializer to include custom logic
  for the 'progress' field, which is a calculated percentage based on the
  elapsed time from the start of the phase until the limit date.
- get_progress: Method that computes the progress value, returning 0%
  if the current date is before the phase's start date, and 100% if the
  current date is after the limit date. The percentage of time passed
  between these two dates is returned otherwise.
"""

import app.selection
from rest_framework import serializers
from app.selection.models.Phase import Phase
from datetime import datetime

from app.selection.models.SelectionSettings import SelectionSettings


class PhaseSerializer(serializers.ModelSerializer):
    """
    Serializer for the Phase model.

    It converts the Phase model instances into JSON format and vice versa,
    and calculates the progress as the percentage of time passed between start_date and limit_date.
    """

    progress = serializers.SerializerMethodField()
    days_elapsed = serializers.SerializerMethodField()
    remaining_days = serializers.SerializerMethodField()

    class Meta:
        model = Phase
        fields = [
            "id",
            "name",
            "number",
            "limit_date",
            "start_date",
            "progress",
            "days_elapsed",
            "remaining_days",
        ]

    def get_progress(self, obj):
        """
        Calculates the progress (percentage) of time passed between start_date and limit_date.
        Returns a value between 0 and 100.

        - Returns 0% if the current date is before the phase's start date.
        - Returns 100% if the current date is after the limit date.
        - Otherwise, returns the percentage of the time elapsed between start_date and limit_date.
        """
        now = datetime.now().date()
        start_date = obj.start_date
        limit_date = obj.limit_date

        if now >= limit_date:
            return 100
        elif now <= start_date:
            return 0

        # Calculate the percentage of time passed
        total_duration = (limit_date - start_date).days
        elapsed_time = (now - start_date).days

        return int((elapsed_time / total_duration) * 100) if total_duration > 0 else 0

    def get_days_elapsed(self, obj):
        """
        Calculates the number of days passed since start_date up to now or limit_date, whichever is
        earlier.
        """
        now = datetime.now().date()
        start_date = obj.start_date
        limit_date = obj.limit_date

        if now < start_date:
            return 0
        elif now >= limit_date:
            return (limit_date - start_date).days
        else:
            return (now - start_date).days

    def get_remaining_days(self, obj):
        """
        Calculates the number of remaining days for the phase based on SelectionSettings.
        """
        if obj.name == app.selection.DECISION:
            phase_days = (
                SelectionSettings.objects.filter(name=app.selection.QUOTES)
                .first()
                .phase_days
            )
        else:
            phase_days = (
                SelectionSettings.objects.filter(name=obj.name).first().phase_days
            )
        days_elapsed = self.get_days_elapsed(obj)
        return max(phase_days - days_elapsed, 0)
