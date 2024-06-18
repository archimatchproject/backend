from rest_framework import serializers
from app.users.models.utils.SupplierSpeciality import SupplierSpeciality


class SupplierSpecialitySerializer(serializers.ModelSerializer):

    
    class Meta:
        model = SupplierSpeciality
        fields = ['label','icon']





