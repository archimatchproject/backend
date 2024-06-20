"""
Module for serializing SliderImage instances using Django REST Framework serializers.
"""

from rest_framework import serializers

from app.cms.models import SliderImage


class SliderImageSerializer(serializers.ModelSerializer):
    """
    Serializer for SliderImage instances.
    """

    class Meta:
        """
        Meta class specifying the model and fields for the serializer.
        """

        model = SliderImage
        fields = ["id", "image"]
