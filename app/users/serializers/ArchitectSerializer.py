from rest_framework import serializers

from app.users.models import Architect
from app.users.serializers.ArchimatchUserSerializer import ArchimatchUserSerializer


class ArchitectSerializer(serializers.ModelSerializer):
    user = ArchimatchUserSerializer(required=True)

    class Meta:
        model = Architect
        fields = "__all__"
