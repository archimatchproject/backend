import environ
import jwt
from rest_framework import status
from rest_framework.exceptions import APIException
from rest_framework.response import Response

from app.users.models import Admin
from app.users.serializers import AdminSerializer

# from app.users.exceptions import UserDataException

env = environ.Env()


class AdminService:
    @classmethod
    def create_admin(cls, data):
        serializer = AdminSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @classmethod
    def update_admin(cls, instance, data):
        serializer = AdminSerializer(instance, data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @classmethod
    def decode_token(cls, token):
        try:
            payload = jwt.decode(token, env("SECRET_KEY"), algorithms=["HS256"])
            return payload
        except Exception as e:
            return {"error": f"Error decoding token: {str(e)}"}

    @classmethod
    def get_admin_by_user_id(cls, user_id):
        try:
            admin = Admin.objects.get(user__id=user_id)
            return admin
        except Admin.DoesNotExist:
            return None

    @classmethod
    def retrieve_by_token(cls, request):
        auth_header = request.META.get("HTTP_AUTHORIZATION")

        if not auth_header or not auth_header.startswith("Bearer "):
            return Response(
                {"error": "Invalid token format"}, status=status.HTTP_401_UNAUTHORIZED
            )

        token = auth_header.split(" ")[1]
        payload = cls.decode_token(token)

        if "error" in payload:
            return Response(
                {"error": payload["error"]}, status=status.HTTP_401_UNAUTHORIZED
            )

        user_id = payload.get("user_id")
        if user_id:
            admin = cls.get_admin_by_user_id(user_id)
            if admin:
                serializer = AdminSerializer(admin)
                return Response(serializer.data)
            return Response(
                {"error": "Admin not found"}, status=status.HTTP_404_NOT_FOUND
            )

        return Response({"message": "Token decoded successfully"})

    @classmethod
    def handle_user_data(self, request_keys, expected_keys):
        if not expected_keys.issubset(request_keys):
            missing_keys = expected_keys - request_keys
            raise APIException(f"Missing keys:".join(missing_keys))

    @classmethod
    def admin_login(cls, request):
        try:
            data = request.data
            request_keys = set(data.keys())
            expected_keys = {"email"}
            cls.handle_user_data(request_keys, expected_keys)

            email = data.get("email")

            if Admin.objects.filter(user__email=email).exists():
                response_data = {
                    "message": "Admin Found",
                    "status_code": status.HTTP_200_OK,
                }
            else:
                response_data = {
                    "message": "Admin Not Found",
                    "status_code": status.HTTP_404_NOT_FOUND,
                }

            return Response(
                response_data.get("message"), status=response_data.get("status_code")
            )
        except APIException as e:
            return Response({"message": str(e)}, status=e.status_code)
        except Exception as e:
            return Response({"message": str(e)}, status=status.HTTP_410_GONE)
