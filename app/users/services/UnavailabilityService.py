"""
Module: announcement Service

This module defines the AnnouncementService class that handles announcement-related operations .

Classes:
    AnnouncementService: Service class for announcement-related operations.

"""

from datetime import datetime
from rest_framework.exceptions import NotFound, ValidationError
from app.users.models.TimeSlot import TimeSlot
from app.users.models.Unavailability import Unavailability
from app.users.serializers.UnavailabilitySerializer import UnavailabilitySerializer
from app.users.models.Admin import Admin
from rest_framework import serializers

class UnavailabilityService:
    """
    Service class for handling announcement-related operations .

    """

    @classmethod
    def create_unavailability(cls, data,user):
        """
        Creates a unavailability for a given announcement and the architect.
        Returns:
            unavailability: The created unavailability instance.

        Raises:
            APIException: If there are issues creating the unavailability.
        """
        try:
            admin = Admin.objects.get(user=user)
            
            date = data.get('date')
            if not date:
                raise ValidationError("The 'date' field is required.")
            
            try:
                datetime.strptime(date, '%Y-%m-%d')
            except ValueError:
                raise ValidationError("Invalid date format. Use 'YYYY-MM-DD'.")

            data["admin"] = admin.id
            existing_unavailability = Unavailability.objects.filter(admin=admin, date=date).first()
            serializer = UnavailabilitySerializer(existing_unavailability, data=data, partial=True)
            print("Serializer data:", data)
            serializer.is_valid(raise_exception=True)
            
            unavailability = serializer.save()
            return unavailability
        except Admin.DoesNotExist as e:
            raise NotFound(detail=str(e))
        except serializers.ValidationError as e:
            raise e
        
    @classmethod
    def get_available_time_slots(cls,request):
        """
        Retrieves the available time slots for a given date.

        This method checks the unavailability records for the specified date and
        filters out the unavailable time slots from the complete list of time slots.
        If any record indicates that the whole day is unavailable, an empty list 
        is returned.

        Args:
            request: The HTTP request object, expected to contain the 'date' query parameter 
                    in 'YYYY-MM-DD' format.

        Returns:
            list: A list of available time slots in 'HH:MM' format for the given date. 
                Returns an empty list if the entire day is unavailable.

        Raises:
            ValidationError: If the 'date' field is missing or the date format is invalid.
            NotFound: If there are issues retrieving required data.
    """
        try:
            date = request.query_params.get('date')
            if not date:
                raise ValidationError("The 'date' field is required.")
            
            try:
                datetime.strptime(date, '%Y-%m-%d')
            except ValueError:
                raise ValidationError("Invalid date format. Use 'YYYY-MM-DD'.")

            all_time_slots = TimeSlot.objects.all()
            unavailability_records = Unavailability.objects.filter(date=date)
            unavailable_time_slots = set()
            whole_day_unavailable = False

            for record in unavailability_records:
                if record.whole_day:
                    whole_day_unavailable = True
                    break
                unavailable_time_slots.update(record.time_slots.values_list('time', flat=True))
            
            if whole_day_unavailable:
                return []
            
            unavailable_time_slots_str = {slot.strftime('%H:%M') for slot in unavailable_time_slots}
            available_time_slots = [
                slot.time.strftime('%H:%M')
                for slot in all_time_slots
                if slot.time.strftime('%H:%M') not in unavailable_time_slots_str
            ]
            
            return available_time_slots
        except Admin.DoesNotExist as e:
            raise NotFound(detail=str(e))
        except serializers.ValidationError as e:
            raise e
