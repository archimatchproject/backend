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

from rest_framework import serializers
from app.selection.models.Phase import Phase
from datetime import datetime

class PhaseSerializer(serializers.ModelSerializer):
    """
    Serializer for the Phase model.

    It converts the Phase model instances into JSON format and vice versa,
    and calculates the progress as the percentage of time passed between start_date and limit_date.
    """
    progress = serializers.SerializerMethodField()

    class Meta:
        model = Phase
        fields = ['id', 'name', 'number', 'limit_date', 'start_date', 'progress']

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
