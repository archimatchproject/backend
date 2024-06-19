import jwt
from rest_framework import status
from rest_framework.exceptions import APIException
from rest_framework.response import Response

from app.users.models import ArchimatchUser, Client
from app.users.serializers import ClientSerializer


# from archimatch_app.exceptions import UserDataException
class ClientService:
    @classmethod
    def handle_user_data(self, request_keys, expected_keys):
        if not expected_keys.issubset(request_keys):
            missing_keys = expected_keys - request_keys
            raise APIException(f"Missing keys:".join(missing_keys))

    @classmethod
    def client_login_email(cls, request):
        try:
            data = request.data
            request_keys = set(data.keys())
            expected_keys = {"email"}
            cls.handle_user_data(request_keys, expected_keys)

            email = data.get("email")

            if Client.objects.filter(user__email=email).exists():
                user = ArchimatchUser.objects.get(username=email)
                if user.password == "":
                    response_data = {
                        "message": {"has_password": False},
                        "status_code": status.HTTP_200_OK,
                    }
                else:
                    response_data = {
                        "message": {"has_password": True},
                        "status_code": status.HTTP_200_OK,
                    }
            else:
                response_data = {
                    "message": "Client Not Found",
                    "status_code": status.HTTP_404_NOT_FOUND,
                }

            return Response(
                response_data.get("message"), status=response_data.get("status_code")
            )
        except APIException as e:
            return Response({"message": str(e)}, status=e.status_code)
        except Exception as e:
            return Response({"message": str(e)}, status=status.HTTP_410_GONE)

    @classmethod
    def client_login_phone(cls, request):
        try:
            data = request.data
            request_keys = set(data.keys())
            expected_keys = {"phone_number"}
            cls.handle_user_data(request_keys, expected_keys)

            phone_number = data.get("phone_number")

            if Client.objects.filter(user__phone_number=phone_number).exists():
                user = ArchimatchUser.objects.get(phone_number=phone_number)
                # TODO: SMS Code verification
                if user.password == "":
                    response_data = {
                        "message": {"has_password": False, "email": user.username},
                        "status_code": status.HTTP_200_OK,
                    }
                else:
                    response_data = {
                        "message": {"has_password": True, "email": user.username},
                        "status_code": status.HTTP_200_OK,
                    }
            else:
                response_data = {
                    "message": "Client Not Found",
                    "status_code": status.HTTP_404_NOT_FOUND,
                }

            return Response(
                response_data.get("message"), status=response_data.get("status_code")
            )
        except APIException as e:
            return Response({"message": str(e)}, status=e.status_code)
        except Exception as e:
            return Response({"message": str(e)}, status=status.HTTP_410_GONE)
