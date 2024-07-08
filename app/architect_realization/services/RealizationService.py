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

from app.architect_realization.models.Realization import Realization
from app.architect_realization.models.RealizationImage import RealizationImage
from app.architect_realization.serializers.RealizationSerializer import RealizationOutputSerializer
from app.architect_realization.serializers.RealizationSerializer import RealizationPOSTSerializer
from app.users.models.Architect import Architect


class RealizationService:
    """
    Service class for handling realization-related operations .

    """

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
            user_id = request.user.id
            if not Architect.objects.filter(user__id=user_id).exists():
                raise NotFound(detail="Architect not found.", code=status.HTTP_404_NOT_FOUND)

            architect = Architect.objects.get(user__id=user_id)
            realization_images = validated_data.pop("realization_images", [])

            with transaction.atomic():
                realization = Realization.objects.create(
                    architect=architect,
                    **validated_data,
                )
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
