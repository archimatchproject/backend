from rest_framework import serializers
from app.announcement.models.utils.PropertyType import PropertyType

class PropertyTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = PropertyType
        fields = ['id', 'label', 'icon', 'project_category']