from rest_framework import serializers
from app.users.models.utils.SocialMedia import SocialMedia


class SocialMediaSerializer(serializers.ModelSerializer):

    
    class Meta:
        model = SocialMedia
        fields = '__all__'





