from rest_framework import serializers


class ArchimatchUserCreatePWSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    password = serializers.CharField(write_only=True)
    confirm_password = serializers.CharField(write_only=True)
