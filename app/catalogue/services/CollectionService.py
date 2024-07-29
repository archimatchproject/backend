"""
Service module for the Collection model.

This module defines the service for handling the business logic and exceptions
related to Collection creation and management.

Classes:
    CollectionService: Service class for Collection operations.
"""

from django.db import transaction

from rest_framework import serializers
from rest_framework import status
from rest_framework.exceptions import APIException
from rest_framework.exceptions import NotFound
from rest_framework.response import Response

from app.catalogue.models.Collection import Collection
from app.catalogue.serializers.CollectionSerializer import CollectionSerializer
from app.users.models.Supplier import Supplier


class CollectionService:
    """
    Service class for handling Collection operations.

    Handles business logic and exception handling for Collection creation and management.

    Methods:
        create_collection(request, data): Handles validation and creation of a new Collection.
    """

    @classmethod
    def create_collection(cls, request, data):
        """
        Handles validation and creation of a new Collection.

        Args:
            request (Request): The request object containing the authenticated user.
            data (dict): The validated data for creating a Collection instance.

        Returns:
            Response: The response object containing the result of the operation.
        """
        serializer = CollectionSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        validated_data = serializer.validated_data

        user = request.user
        try:
            supplier = Supplier.objects.get(user=user)
            with transaction.atomic():
                # Create Collection instance
                collection = Collection.objects.create(supplier=supplier, **validated_data)

                return Response(
                    CollectionSerializer(collection).data,
                    status=status.HTTP_201_CREATED,
                )
        except Supplier.DoesNotExist:
            raise NotFound(detail="Authenticated user is not a supplier.")
        except serializers.ValidationError as e:
            raise e
        except Exception as e:
            raise APIException(detail=f"Error creating collection: {str(e)}")
