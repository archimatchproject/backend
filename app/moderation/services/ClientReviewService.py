"""
Service module for the ClientReview model.

This module defines the service for handling the business logic and exceptions
related to ClientReview creation and management.

Classes:
    ClientReviewService: Service class for ClientReview operations.
"""

from django.db import IntegrityError
from django.db import transaction

from rest_framework import serializers
from rest_framework import status
from rest_framework.exceptions import APIException
from rest_framework.exceptions import NotFound
from rest_framework.response import Response

from app.moderation.models.ClientReview import ClientReview
from app.moderation.serializers.ClientReviewSerializer import ClientReviewSerializer
from app.users.models.Architect import Architect
from app.users.models.Client import Client


class ClientReviewService:
    """
    Service class for handling ClientReview operations.

    Handles business logic and exception handling for ClientReview creation and management.

    Methods:
        create_client_review(request): Handles validation and creation of a new ClientReview.
    """

    @classmethod
    def create_client_review(cls, request):
        """
        Handles validation and creation of a new ClientReview.

        Args:
            request (Request): The request object containing the authenticated user.

        Returns:
            Response: The response object containing the result of the operation.
        """
        serializer = ClientReviewSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        validated_data = serializer.validated_data

        user = request.user
        try:
            client = Client.objects.get(user=user)
            with transaction.atomic():
                # Create ClientReview instance
                client_review = ClientReview.objects.create(
                    client=client, architect=validated_data.pop("architect_id"), **validated_data
                )

                return Response(
                    ClientReviewSerializer(client_review).data,
                    status=status.HTTP_201_CREATED,
                )
        except IntegrityError as e:
            if "unique constraint" in str(e):
                raise serializers.ValidationError(
                    {"detail": "A review for this architect by this client already exists."}
                )
            raise APIException(detail=f"Error creating client review : {str(e)}")
        except Client.DoesNotExist:
            raise NotFound(detail="Authenticated user is not a client.")
        except serializers.ValidationError as e:
            raise e
        except Exception as e:
            raise APIException(detail=f"Error creating client review: {str(e)}")

    @classmethod
    def get_architect_reviews(cls, request):
        """
        Retrieves reviews for the architect associated with the provided token.

        Args:
            request (Request): The request object containing the authenticated user's token.

        Returns:
            Response: A response object containing the list of reviews for the architect.
        """
        user = request.user

        try:
            architect = Architect.objects.get(user=user)
            reviews = ClientReview.objects.filter(architect=architect)
            serialized_reviews = ClientReviewSerializer(reviews, many=True)
            return Response(serialized_reviews.data)
        except Architect.DoesNotExist:
            raise NotFound(detail="Authenticated user is not an architect.")
        except Exception as e:
            raise APIException(detail=f"Error retrieving architect reviews: {str(e)}")
