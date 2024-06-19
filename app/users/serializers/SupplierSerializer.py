from rest_framework import serializers

from app.users.models import Supplier
from app.users.serializers.ArchimatchUserSerializer import ArchimatchUserSerializer
from app.users.serializers.utils.SocialMediaSerializer import SocialMediaSerializer


class SupplierSerializer(serializers.ModelSerializer):
    user = ArchimatchUserSerializer(required=True)
    social_links = SocialMediaSerializer()

    class Meta:
        model = Supplier
        fields = "__all__"
