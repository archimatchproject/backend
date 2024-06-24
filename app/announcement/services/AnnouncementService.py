"""
Module: announcement Service

This module defines the AnnouncementService class that handles announcement-related operations .

Classes:
    AnnouncementService: Service class for announcement-related operations.

"""

from rest_framework import status
from rest_framework.exceptions import APIException
from rest_framework.response import Response

from app.announcement import BUDGETS, CITIES, TERRAIN_SURFACES, WORK_SURFACES
from app.announcement.models.AnnouncementWorkType import AnnouncementWorkType
from app.announcement.models.ArchitectSpeciality import ArchitectSpeciality
from app.announcement.models.ArchitecturalStyle import ArchitecturalStyle
from app.announcement.models.Need import Need
from app.announcement.models.PieceRenovate import PieceRenovate
from app.announcement.models.ProjectCategory import ProjectCategory
from app.announcement.models.ProjectExtension import ProjectExtension
from app.announcement.models.PropertyType import PropertyType
from app.announcement.serializers.AnnouncementWorkTypeSerializer import (
    AnnouncementWorkTypeSerializer,
)
from app.announcement.serializers.ArchitectSpecialitySerializer import (
    ArchitectSpecialitySerializer,
)
from app.announcement.serializers.ArchitecturalStyleSerializer import (
    ArchitecturalStyleSerializer,
)
from app.announcement.serializers.NeedSerializer import NeedSerializer
from app.announcement.serializers.PieceRenovateSerializer import PieceRenovateSerializer
from app.announcement.serializers.ProjectCategorySerializer import (
    ProjectCategorySerializer,
)
from app.announcement.serializers.ProjectExtensionSerializer import (
    ProjectExtensionSerializer,
)
from app.announcement.serializers.PropertyTypeSerializer import PropertyTypeSerializer


class AnnouncementService:
    """
    Service class for handling announcement-related operations .

    """

    @classmethod
    def handle_user_data(cls, request_keys, expected_keys):
        """
        Validates the presence of expected keys in request data.

        Args:
            request_keys (set): Set of keys present in the request data.
            expected_keys (set): Set of keys expected to be present in the request data.

        Raises:
            APIException: If any expected key is missing in the request data.
        """
        if not expected_keys.issubset(request_keys):
            missing_keys = expected_keys - request_keys
            raise APIException(f"Missing keys: {', '.join(missing_keys)}")

    @classmethod
    def get_architect_specialities(cls):
        """
        Retrieves all architect specialities.

        Returns:
            Response: Response containing list of architect specialities.
        """
        try:
            architect_specialities = ArchitectSpeciality.objects.all()
            serializer = ArchitectSpecialitySerializer(
                architect_specialities, many=True
            )
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            raise APIException(f"Error retrieving architect specialities: {str(e)}")

    @classmethod
    def get_architect_speciality_needs(cls, architect_speciality_id):
        """
        Retrieves needs based on architect speciality.

        Args:
            architect_speciality_id (int): ID of the architect speciality.

        Returns:
            Response: Response containing list of needs related to the architect speciality.
        """
        try:
            needs = Need.objects.filter(architect_speciality_id=architect_speciality_id)
            serializer = NeedSerializer(needs, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            raise APIException(f"Error retrieving architect speciality needs: {str(e)}")

    @classmethod
    def get_project_categories(cls):
        """
        Retrieves all project categories.

        Returns:
        Response: Response containing list of project categories.
        """
        try:
            project_categories = ProjectCategory.objects.all()
            serializer = ProjectCategorySerializer(project_categories, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            raise APIException(f"Error retrieving project categories: {str(e)}")

    @classmethod
    def get_property_types(cls, project_category_id):
        """
        Retrieves property types based on project category.

        Args:
            project_category_id (int): ID of the project category.

        Returns:
            Response: Response containing list of property types related to the project category.
        """
        try:
            property_types = PropertyType.objects.filter(
                project_category_id=project_category_id
            )
            serializer = PropertyTypeSerializer(property_types, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            raise APIException(f"Error retrieving property types: {str(e)}")

    @classmethod
    def get_announcement_work_types(cls):
        """
        Retrieves all announcement work types.

        Returns:
            Response: Response containing list of announcement work types.
        """
        try:
            announcement_work_types = AnnouncementWorkType.objects.all()
            serializer = AnnouncementWorkTypeSerializer(
                announcement_work_types, many=True
            )
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            raise APIException(f"Error retrieving announcement work types: {str(e)}")

    @classmethod
    def get_renovation_pieces(cls):
        """
        Retrieves all renovation pieces.

        Returns:
            Response: Response containing list of renovation pieces.
        """
        try:
            renovation_pieces = PieceRenovate.objects.all()
            serializer = PieceRenovateSerializer(renovation_pieces, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            raise APIException(f"Error retrieving renovation pieces: {str(e)}")

    @classmethod
    def get_cities(cls):
        """
        Retrieves predefined cities choices.

        Returns:
            Response: Response containing list of cities.
        """
        cities = [{"value": city[0], "display_name": city[1]} for city in CITIES]
        return Response(cities, status=status.HTTP_200_OK)

    @classmethod
    def get_terrain_surfaces(cls):
        """
        Retrieves predefined terrain surfaces choices.

        Returns:
            Response: Response containing list of terrain surfaces.
        """
        terrain_surfaces = [
            {"value": surface[0], "display_name": surface[1]}
            for surface in TERRAIN_SURFACES
        ]
        return Response(terrain_surfaces, status=status.HTTP_200_OK)

    @classmethod
    def get_work_surfaces(cls):
        """
        Retrieves predefined work surfaces choices.

        Returns:
            Response: Response containing list of work surfaces.
        """
        work_surfaces = [
            {"value": surface[0], "display_name": surface[1]}
            for surface in WORK_SURFACES
        ]
        return Response(work_surfaces, status=status.HTTP_200_OK)

    @classmethod
    def get_budgets(cls):
        """
        Retrieves predefined budgets choices.

        Returns:
            Response: Response containing list of budgets.
        """
        budgets = [
            {"value": budget[0], "display_name": budget[1]} for budget in BUDGETS
        ]
        return Response(budgets, status=status.HTTP_200_OK)

    @classmethod
    def get_architectural_styles(cls):
        """
        Retrieves all architectural styles.

        Returns:
            Response: Response containing list of architectural styles.
        """
        try:
            architectural_styles = ArchitecturalStyle.objects.all()
            serializer = ArchitecturalStyleSerializer(architectural_styles, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response(
                {"message": f"Error retrieving architectural styles: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

    @classmethod
    def get_project_extensions(cls):
        """
        Retrieves all project extensions.

        Returns:
            Response: Response containing list of project extensions.
        """
        try:
            project_extensions = ProjectExtension.objects.all()
            serializer = ProjectExtensionSerializer(project_extensions, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response(
                {"message": f"Error retrieving project extensions: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
