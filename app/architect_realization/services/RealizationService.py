"""
Module: Realization Service

This module defines the RealizationService class that handles Realization-related operations .

Classes:
    RealizationService: Service class for Realization-related operations.

"""

from django.db import transaction

from rest_framework import serializers
from rest_framework import status
from rest_framework.exceptions import APIException
from rest_framework.exceptions import NotFound
from rest_framework.response import Response

from app.announcement.models.Need import Need
from app.announcement.serializers.ArchitecturalStyleSerializer import ArchitecturalStyleSerializer
from app.announcement.serializers.NeedSerializer import NeedSerializer
from app.architect_realization.models.Realization import Realization
from app.architect_realization.models.RealizationImage import RealizationImage
from app.architect_realization.serializers.RealizationSerializer import RealizationOutputSerializer
from app.architect_realization.serializers.RealizationSerializer import RealizationPOSTSerializer
from app.core.models.ArchitectSpeciality import ArchitectSpeciality
from app.core.models.ArchitecturalStyle import ArchitecturalStyle
from app.core.pagination import CustomPagination
from app.users.models.Architect import Architect


class RealizationService:
    """
    Service class for handling realization-related operations .

    """

    pagination_class = CustomPagination

    @classmethod
    def realization_create(cls, request):
        """
        Creating new realization
        """
        data = request.data
        serializer = RealizationPOSTSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        validated_data = serializer.validated_data

        try:
            needs_data = validated_data.pop("needs")
            user_id = request.user.id
            if not Architect.objects.filter(user__id=user_id).exists():
                raise NotFound(detail="Architect not found.", code=status.HTTP_404_NOT_FOUND)

            architect = Architect.objects.get(user__id=user_id)
            realization_images = request.FILES.getlist("realization_images", [])

            with transaction.atomic():
                realization = Realization.objects.create(
                    architect=architect,
                    **validated_data,
                )
                realization.needs.set(needs_data)
                for image in realization_images:
                    RealizationImage.objects.create(
                        realization=realization,
                        image=image,
                    )
            return Response(
                {
                    "message": "Realization created successfully",
                    "data": RealizationOutputSerializer(realization).data,
                },
                status=status.HTTP_201_CREATED,
            )
        except serializers.ValidationError as e:
            raise e
        except Exception as e:
            raise APIException(detail=str(e))

    @classmethod
    def get_architectural_styles(cls):
        """
        Retrieves all architectural styles.

        Returns:
            Response: Response containing list of architectural styles.
        """
        try:
            architectural_styles = ArchitecturalStyle.objects.all()
            serializer = ArchitecturalStyleSerializer(
                architectural_styles,
                many=True,
            )
            return Response(
                serializer.data,
                status=status.HTTP_200_OK,
            )
        except Exception:
            return APIException(detail="Error retrieving architectural styles")

    @classmethod
    def get_architect_speciality_needs(cls, request):
        """
        Retrieves needs based on architect speciality.

        Args:
            architect_speciality_id (int): ID of the architect speciality.

        Returns:
            Response: Response containing list of needs related to the architect speciality.
        """
        try:
            user_id = request.user.id
            architect = Architect.objects.get(user__id=user_id)

            needs = Need.objects.filter(architect_speciality_id=architect.architect_speciality.id)
            serializer = NeedSerializer(needs, many=True)

            return Response(
                serializer.data,
                status=status.HTTP_200_OK,
            )
        except Architect.DoesNotExist:
            raise NotFound(detail="Architect not found.")
        except ArchitectSpeciality.DoesNotExist:
            raise NotFound(detail="No architect speciality found with the given ID")
        except Exception:
            raise APIException(detail="Error retrieving architect speciality needs")

    @classmethod
    def get_realizations_by_category(cls, request, id):
        """
        Retrieves needs based on architect speciality.

        Args:
            architect_speciality_id (int): ID of the architect speciality.

        Returns:
            Response: Response containing list of needs related to the architect speciality.
        """
        try:
            realizations = Realization.objects.filter(project_category__id=id)
            paginator = cls.pagination_class()
            page = paginator.paginate_queryset(realizations, request)
            if page is not None:
                serializer = RealizationOutputSerializer(page, many=True)
                return paginator.get_paginated_response(serializer.data)
            serializer = RealizationOutputSerializer(realizations, many=True)
            return Response(
                serializer.data,
                status=status.HTTP_200_OK,
            )
        except Realization.DoesNotExist:
            raise NotFound(detail="Realizations not found.")
        except Exception as e:
            raise APIException(detail=str(e))

    @classmethod
    def get_realizations_by_architect(cls, request, id):
        """
        Retrieves needs based on architect speciality.

        Args:
            architect_speciality_id (int): ID of the architect speciality.

        Returns:
            Response: Response containing list of needs related to the architect speciality.
        """
        try:
            realizations = Realization.objects.filter(architect__id=id)
            paginator = cls.pagination_class()
            page = paginator.paginate_queryset(realizations, request)
            if page is not None:
                serializer = RealizationOutputSerializer(page, many=True)
                return paginator.get_paginated_response(serializer.data)
            serializer = RealizationOutputSerializer(realizations, many=True)
            return Response(
                serializer.data,
                status=status.HTTP_200_OK,
            )
        except Realization.DoesNotExist:
            raise NotFound(detail="Realizations not found.")
        except Exception as e:
            raise APIException(detail=str(e))
