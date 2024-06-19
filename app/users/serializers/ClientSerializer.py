from rest_framework import serializers

from app.users.models import ArchimatchUser, Client
from app.users.serializers.ArchimatchUserSerializer import ArchimatchUserSerializer


class ClientSerializer(serializers.ModelSerializer):
    user = ArchimatchUserSerializer()

    class Meta:
        model = Client
        fields = ["id", "user"]

    def create(self, validated_data):
        user_data = validated_data.pop("user")
        user = ArchimatchUser.objects.create(**user_data)
        client = Client.objects.create(user=user, **validated_data)
        return client

    def update(self, instance, validated_data):
        user_data = validated_data.pop("user")
        user = instance.user

        instance.user.username = user_data.get("username", user.username)
        instance.user.first_name = user_data.get("first_name", user.first_name)
        instance.user.last_name = user_data.get("last_name", user.last_name)
        instance.user.email = user_data.get("email", user.email)
        instance.user.phone_number = user_data.get("phone_number", user.phone_number)
        instance.user.image = user_data.get("image", user.image)
        instance.user.user_type = user_data.get("user_type", user.user_type)
        instance.user.save()

        instance.save()
        return instance
