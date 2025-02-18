from rest_framework import serializers
from app.officeOffer.models.SoftwareSkill import SoftwareSkill


class SoftwareSkillSerializer(serializers.ModelSerializer):
    """
    Serializer class for SoftwareSkill model.
    """

    class Meta:
        """
        Meta class for SoftwareSkillSerializer.

        Specifies the model to be serialized and the fields to be included in the serialization.
        """
        model = SoftwareSkill
        fields = ["id", "label"]
