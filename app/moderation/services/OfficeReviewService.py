"""
Service module for the OfficeReview model.

Handles business logic and exception handling for OfficeReview creation and statistics.

Classes:
    OfficeReviewService: Service class for OfficeReview operations.
"""

from django.db import IntegrityError
from django.db import transaction

from rest_framework import serializers
from rest_framework.exceptions import APIException
from rest_framework.exceptions import NotFound

from app.core.pagination import CustomPagination
from app.moderation.models import OfficeReview
from app.moderation.serializers import OfficeReviewSerializer
from app.users.models import Architect
from app.users.models.Office import Office


class OfficeReviewService:
    """
    Service class for handling OfficeReview operations.

    Methods:
        create_office_review(request): Handles validation and creation of a new OfficeReview.
        get_architect_reviews(request): Retrieves reviews for an architect.
        get_architect_statistics(request): Generates statistics for an architect.
    """

    pagination_class = CustomPagination

    @classmethod
    def create_office_review(cls, request):
        """
        Handles validation and creation of a new OfficeReview.

        Args:
            request (Request): The request object containing the authenticated user.

        Returns:
            tuple: A boolean success flag and response data.
        """
        serializer = OfficeReviewSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        validated_data = serializer.validated_data

        user = request.user
        try:
            office = Office.objects.get(user=user)
            with transaction.atomic():
                # Create OfficeReview instance
                office_review = OfficeReview.objects.create(
                    office=office,
                    architect=validated_data.pop("architect_id"),
                    **validated_data,
                )

                return True, OfficeReviewSerializer(office_review).data

        except IntegrityError as e:
            if "unique constraint" in str(e):
                raise serializers.ValidationError(
                    {"detail": "A review for this architect by this office already exists."}
                )
            raise APIException(detail=f"Error creating office review: {str(e)}")
        except Office.DoesNotExist:
            raise NotFound(detail="Authenticated user is not an office.")
        except serializers.ValidationError as e:
            raise e
        except Exception as e:
            raise APIException(detail=f"Error creating office review: {str(e)}")

    @classmethod
    def get_architect_reviews(cls, request):
        """
        Retrieves reviews for the architect associated with the provided token.

        Args:
            request (Request): The request object containing the authenticated user's token.

        Returns:
            tuple: A boolean success flag and response data.
        """
        user = request.user

        architect = Architect.objects.get(user=user)
        reviews = OfficeReview.objects.filter(architect=architect)
        serialized_reviews = OfficeReviewSerializer(reviews, many=True)
        return True, serialized_reviews.data

    @classmethod
    def get_architect_statistics(cls, request):
        """
        Generates statistics for an architect's reviews.

        Args:
            request (Request): The request object containing the architect ID.

        Returns:
            tuple: A boolean success flag and response data.
        """
        user = request.user

        architect = Architect.objects.get(user=user)
        reviews = OfficeReview.objects.filter(architect=architect)

        # Count the occurrences of each rating (1, 2, 3)
        rating_counts = {1: 0, 2: 0, 3: 0}
        for review in reviews:
            rating_counts[review.rating] += 1

        # Determine the dominant rating
        dominant_rating = max(rating_counts, key=rating_counts.get) if reviews else None

        return True, {
            "ratings": rating_counts,
            "dominant_rating": dominant_rating,
        }
