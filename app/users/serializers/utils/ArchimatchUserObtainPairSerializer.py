from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from app.users.serializers import ArchimatchUserSerializer


class ArchimatchUserObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        token["user"] = ArchimatchUserSerializer(user).data

        return token
