"""
Module: announcement Service

This module defines the AnnouncementService class that handles announcement-related operations .

Classes:
    AnnouncementService: Service class for announcement-related operations.

"""

from datetime import datetime
from rest_framework.exceptions import NotFound, ValidationError
from app.users.models.Meeting import Meeting
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
    def create_unavailability(cls, data_list, user):
        """
        Creates multiple unavailabilities for a given admin and date.

        Args:
            data_list: List of dictionaries containing unavailability data.
            user: The user making the request.

        Returns:
            List of created or updated unavailability instances.

        Raises:
            ValidationError: If validation fails.
            NotFound: If the admin is not found.
        """
        created_unavailabilities = []

        
        admin = Admin.objects.get(user=user)

        for data in data_list:
            date = data.get('date')
            if not date:
                raise ValidationError("The 'date' field is required.")
            
            try:
                datetime.strptime(date, '%Y-%m-%d')
            except ValueError:
                raise ValidationError("Invalid date format. Use 'YYYY-MM-DD'.")

            data["admin"] = admin.id
            existing_unavailability = Unavailability.objects.filter(admin=admin, date=date).first()
            
            # If an existing unavailability is found, update it, otherwise create a new one
            if existing_unavailability:
                serializer = UnavailabilitySerializer(existing_unavailability, data=data, partial=True)
            else:
                serializer = UnavailabilitySerializer(data=data)
            
            serializer.is_valid(raise_exception=True)
            
            unavailability = serializer.save()
            created_unavailabilities.append(unavailability)
        return True,"unavailability created successfully."

        
    @classmethod
    def get_available_time_slots(cls, request):
        """
        Retrieves the available time slots for a given date across all admins.

        This method checks the unavailability records for the specified date and
        filters out the unavailable time slots from the complete list of time slots.
        It also filters out time slots that are already booked by meetings. 
        If all relevant records indicate that the whole day is unavailable for all admins, 
        an empty list is returned.

        Args:
            request: The HTTP request object, expected to contain the 'date' query parameter 
                    in 'YYYY-MM-DD' format.

        Returns:
            list: A list of available time slots in 'HH:MM' format for the given date. 
                Returns an empty list if the entire day is unavailable for all admins.

        Raises:
            ValidationError: If the 'date' field is missing or the date format is invalid.
            NotFound: If there are issues retrieving required data.
        """
        
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
        whole_day_unavailable_admins = set()

        for record in unavailability_records:
            if record.whole_day:
                whole_day_unavailable_admins.add(record.admin.id)
            else:
                unavailable_time_slots.update(record.time_slots.values_list('time', flat=True))

        # If all admins marked the day as unavailable, return an empty list
        if len(whole_day_unavailable_admins) == Admin.objects.count():
            return []

        # Exclude time slots that have scheduled meetings on the same date
        booked_time_slots = Meeting.objects.filter(date=date).values_list('time__time', flat=True)
        unavailable_time_slots.update(booked_time_slots)

        unavailable_time_slots_str = {slot.strftime('%H:%M') for slot in unavailable_time_slots}
        available_time_slots = [
            slot.time.strftime('%H:%M')
            for slot in all_time_slots
            if slot.time.strftime('%H:%M') not in unavailable_time_slots_str
        ]

        return True,available_time_slots
        
