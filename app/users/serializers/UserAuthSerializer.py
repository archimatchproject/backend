from rest_framework import serializers


class UserAuthSerializer(serializers.Serializer):
    email = serializers.EmailField()


class UserAuthPhoneSerializer(serializers.Serializer):
    phone_number = serializers.CharField()
