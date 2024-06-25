"""
Module: announcement Service

This module defines the AnnouncementService class that handles announcement-related operations .

Classes:
    AnnouncementService: Service class for announcement-related operations.

"""

from django.db import transaction
from django.shortcuts import get_object_or_404

from rest_framework import status
from rest_framework.exceptions import APIException
from rest_framework.response import Response

from app.announcement import BUDGETS, CITIES, TERRAIN_SURFACES, WORK_SURFACES
from app.announcement.models.Announcement import Announcement
from app.announcement.models.AnnouncementPieceRenovate import AnnouncementPieceRenovate
from app.announcement.models.AnnouncementWorkType import AnnouncementWorkType
from app.announcement.models.ArchitectSpeciality import ArchitectSpeciality
from app.announcement.models.ArchitecturalStyle import ArchitecturalStyle
from app.announcement.models.Need import Need
from app.announcement.models.PieceRenovate import PieceRenovate
from app.announcement.models.ProjectCategory import ProjectCategory
from app.announcement.models.ProjectExtension import ProjectExtension
from app.announcement.models.ProjectImage import ProjectImage
from app.announcement.models.PropertyType import PropertyType
from app.announcement.serializers.AnnouncementSerializer import (
    AnnouncementOutputSerializer,
    AnnouncementPOSTSerializer,
    AnnouncementPUTSerializer,
)
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
from app.users import USER_TYPE_CHOICES
from app.users.models import Client
from app.users.models.ArchimatchUser import ArchimatchUser


class AnnouncementService:
    """
    Service class for handling announcement-related operations .

    """

    @classmethod
    def create_announcement(cls, data):
        """
        Creating new announcement
        """
        serializer = AnnouncementPOSTSerializer(data=data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        validated_data = serializer.validated_data

        try:
            needs_data = validated_data.pop("needs")
            pieces_renovate_data = validated_data.pop("pieces_renovate", [])
            project_extensions_data = validated_data.pop("project_extensions")
            project_images_data = validated_data.pop("project_images", [])
            client_data = validated_data.pop("client", None)

            with transaction.atomic():
                if client_data:
                    user_data = client_data.pop("user")
                    user_data["username"] = user_data["email"]
                    user_data["user_type"] = USER_TYPE_CHOICES[1][0]
                    user_instance = ArchimatchUser.objects.create_user(**user_data)
                    client_instance = Client.objects.create(
                        user=user_instance, **client_data
                    )
                else:
                    client_instance = None

                announcement = Announcement.objects.create(
                    client=client_instance, **validated_data
                )
                announcement.needs.set(needs_data)

                for piece_data in pieces_renovate_data:
                    piece_renovate_id = piece_data["piece_renovate"]
                    piece_renovate = PieceRenovate.objects.get(pk=piece_renovate_id)
                    AnnouncementPieceRenovate.objects.create(
                        announcement=announcement,
                        piece_renovate=piece_renovate,
                        number=piece_data["number"],
                    )

                announcement.project_extensions.set(project_extensions_data)

                for image in project_images_data:
                    ProjectImage.objects.create(announcement=announcement, image=image)

            return Response(
                {
                    "message": "Announcement created successfully",
                    "data": AnnouncementOutputSerializer(announcement).data,
                },
                status=status.HTTP_201_CREATED,
            )
        except Exception as e:
            raise APIException(f"Error creating announcement")

    @classmethod
    def update_announcement(cls, instance, data):
        """
        Updating existing announcement
        """
        serializer = AnnouncementPUTSerializer(instance, data=data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        validated_data = serializer.validated_data

        try:
            needs_data = validated_data.pop("needs")
            pieces_renovate_data = validated_data.pop("pieces_renovate", [])
            project_extensions_data = validated_data.pop("project_extensions")
            project_images_data = validated_data.pop("project_images", [])

            instance.needs.set(needs_data)

            AnnouncementPieceRenovate.objects.filter(announcement=instance).delete()
            for piece_data in pieces_renovate_data:
                piece_renovate_id = piece_data["piece_renovate"]
                piece_renovate = PieceRenovate.objects.get(pk=piece_renovate_id)
                AnnouncementPieceRenovate.objects.create(
                    announcement=instance,
                    piece_renovate=piece_renovate,
                    number=piece_data["number"],
                )

            instance.project_extensions.set(project_extensions_data)

            ProjectImage.objects.filter(announcement=instance).delete()
            for image in project_images_data:
                ProjectImage.objects.create(announcement=instance, image=image)

            for attr, value in validated_data.items():
                setattr(instance, attr, value)
            instance.save()

            return Response(
                {
                    "message": "Announcement updated successfully",
                    "data": AnnouncementOutputSerializer(instance).data,
                },
                status=status.HTTP_200_OK,
            )
        except Exception as e:
            raise APIException(f"Error updating announcement")

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
            raise APIException(f"Error retrieving architect specialities")

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
            if not ArchitectSpeciality.objects.filter(
                id=architect_speciality_id
            ).exists():
                return Response(
                    {"message": "No architect speciality found with the given ID"},
                    status=status.HTTP_404_NOT_FOUND,
                )
            needs = Need.objects.filter(architect_speciality_id=architect_speciality_id)
            serializer = NeedSerializer(needs, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            raise APIException(f"Error retrieving architect speciality needs")

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
            raise APIException(f"Error retrieving project categories")

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
            if not ProjectCategory.objects.filter(id=project_category_id).exists():
                return Response(
                    {"message": "No project category found with the given ID"},
                    status=status.HTTP_404_NOT_FOUND,
                )
            property_types = PropertyType.objects.filter(
                project_category_id=project_category_id
            )
            serializer = PropertyTypeSerializer(property_types, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            raise APIException(f"Error retrieving property types")

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
            raise APIException(f"Error retrieving announcement work types")

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
            raise APIException(f"Error retrieving renovation pieces")

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
                {"message": f"Error retrieving architectural styles"},
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
                {"message": f"Error retrieving project extensions"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
