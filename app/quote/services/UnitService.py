"""
UnitService Module
This module provides a service class for handling operations related to Unit objects.
It includes methods for creating a unit, retrieving all units, and deleting a unit.

Classes:
    UnitService: A service class for managing Unit operations.
"""

from rest_framework.exceptions import APIException

from app.quote.models.Unit import Unit
from app.quote.serializers.UnitSerializer import UnitSerializer


class UnitService:
    """
    Service class for handling Unit operations.

    This class provides methods to create a unit, retrieve all units, and delete a unit.
    """

    @classmethod
    def get_all_units(cls):
        """
        Retrieve and return a paginated list of all units.

        Args:
            request (HttpRequest): The incoming HTTP request.

        Returns:
            tuple: (True, data) where data is a list of paginated unit data.
        """

        units = Unit.objects.all().order_by("-created_at")
        serializer = UnitSerializer(units, many=True)
        return True, serializer.data

    @classmethod
    def create_unit(cls, data):
        """
        Create a new unit.

        Args:
            title (str): The title for the new unit.

        Returns:
            tuple: (True, data) where data is a success message or unit information.

        Raises:
            APIException: If there is an issue with creating the unit.
        """

        title = data.get("title")
        if title in None:
            raise APIException("Title is required to create a unit.")

        unit = Unit.objects.create(title=title)
        unit_data = UnitSerializer(unit).data
        return True, unit_data

    @classmethod
    def delete_unit(cls, unit_id):
        """
        Delete a unit by its ID.

        Args:
            unit_id (int): The ID of the unit to be deleted.

        Returns:
            tuple: (True, data) where data is a success message or an error message if the unit was not found.

        Raises:
            APIException: If there is an issue with deleting the unit or if the unit is not found.
        """
        try:
            unit = Unit.objects.get(id=unit_id)
            unit.delete()
            return True, "Unit deleted successfully."
        except Unit.DoesNotExist:
            raise APIException("Unit not found.")
