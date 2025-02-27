"""
Serializer for architect office review statistics.
This module defines the serializer used for sending architect review statistics,
including ratings count, dominant rating, total reviews, average rating, and detailed reviews.
"""

from rest_framework import serializers

from app.moderation.serializers.OfficeReviewSerializer import OfficeReviewSerializer


class ArchitectOfficeStatisticsSerializer(serializers.Serializer):
    """
    Serializer for architect review statistics.
    """

    ratings = serializers.DictField(child=serializers.IntegerField(), help_text="Count of each rating (1, 2, 3).")
    dominant_rating = serializers.IntegerField(allow_null=True, help_text="Most frequent rating.")
    total_reviews = serializers.IntegerField(help_text="Total number of reviews for the architect.")
    average_rating = serializers.FloatField(help_text="Average rating of all reviews.")
    reviews = OfficeReviewSerializer(many=True)
