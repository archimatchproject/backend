from rest_framework import serializers

from app.announcement.models.utils.PieceRenovate import PieceRenovate


class PieceRenovateSerializer(serializers.ModelSerializer):
    class Meta:
        model = PieceRenovate
        fields = ["id", "label", "icon", "number"]
