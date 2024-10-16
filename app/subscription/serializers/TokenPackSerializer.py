"""
Serializer module for the TokenPack model.
"""

from rest_framework import serializers

from app.subscription.models.TokenPack import TokenPack


class TokenPackSerializer(serializers.ModelSerializer):
    """
    Serializer for the TokenPack model.
    """

    class Meta:
        """
        Meta class for TokenPackSerializer.
        """

        model = TokenPack
        fields = ["id", "pack_name", "pack_price", "number_tokens", "number_free_tokens", "active"]
