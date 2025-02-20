from rest_framework import serializers
from app.officeOffer.models.TechnicalSkill import TechnicalSkill


class TechnicalSkillSerializer(serializers.ModelSerializer):
    """
    Serializer class for TechnicalSkill model.
    """

    class Meta:
        """
        Meta class for TechnicalSkillSerializer.

        Specifies the model to be serialized and the fields to be included in the serialization.
        """
        model = TechnicalSkill
        fields = ["id", "label"]
