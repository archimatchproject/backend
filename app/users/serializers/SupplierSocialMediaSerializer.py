from rest_framework import serializers

from app.users.models.SupplierSocialMedia import SupplierSocialMedia


class SupplierSocialMediaSerializer(serializers.ModelSerializer):
    class Meta:
        model = SupplierSocialMedia
        fields = "__all__"
