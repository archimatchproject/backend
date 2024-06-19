from rest_framework import serializers

from app.users.models import ArchimatchUser


class ArchimatchUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = ArchimatchUser
        fields = [
            "username",
            "first_name",
            "last_name",
            "email",
            "phone_number",
            "image",
            "user_type",
        ]


class ArchimatchUserSimpleSerializer(serializers.ModelSerializer):
    class Meta:
        model = ArchimatchUser
        fields = ["first_name", "last_name", "email", "phone_number"]
