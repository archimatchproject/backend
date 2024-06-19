from rest_framework import serializers

from app.users.models import Supplier
from app.users.serializers.ArchimatchUserSerializer import ArchimatchUserSerializer
from app.users.serializers.SupplierSocialMediaSerializer import (
    SupplierSocialMediaSerializer,
)


class SupplierSerializer(serializers.ModelSerializer):
    user = ArchimatchUserSerializer(required=True)
    social_links = SupplierSocialMediaSerializer()

    class Meta:
        model = Supplier
        fields = "__all__"
