from rest_framework import serializers
from app.users.models import Admin,ArchimatchUser
from app.users.serializers.ArchimatchUserSerializer import ArchimatchUserSerializer

class AdminSerializer(serializers.ModelSerializer):
    user = ArchimatchUserSerializer()
    rights = serializers.ListField(
        child=serializers.CharField(max_length=100),
        required=True,
        write_only=True
    )
    
    class Meta:
        model = Admin
        fields = ['id','super_user','user', 'rights']

    
    def create(self, validated_data):
        rights = validated_data.pop('rights', [])
        user_data = validated_data.pop('user')
        user = ArchimatchUser.objects.create(**user_data)
        admin = Admin.objects.create(user=user, **validated_data)
        admin.set_permissions(rights)
        return admin

    def update(self, instance, validated_data):
        rights = validated_data.pop('rights', None)
        user_data = validated_data.pop('user', None)
        if user_data:
            for attr, value in user_data.items():
                setattr(instance.user, attr, value)
            instance.user.save()
        if rights is not None:
            instance.permissions.clear()
            instance.set_permissions(rights)
        return super().update(instance, validated_data)
    
    def to_representation(self, instance):
        data = super().to_representation(instance)
        if instance.super_user:
            data['rights'] = ['__All__']
        else:
            data['rights'] = list(instance.permissions.values_list('codename', flat=True))
        return data
