from rest_framework import status

# from app.users.exceptions import UserDataException
from rest_framework.exceptions import APIException
from rest_framework.response import Response

from app.users.models import ArchimatchUser


class ArchimatchUserService:
    @classmethod
    def handle_user_data(self, request_keys, expected_keys):
        if not expected_keys.issubset(request_keys):
            missing_keys = (expected_keys - request_keys,)
            raise APIException(f"Missing keys:".join(missing_keys))

    @classmethod
    def create_password(self, request):
        try:

            data = request.data
            request_keys = set(data.keys())
            expected_keys = {"id", "password", "confirm_password"}
            ArchimatchUserService.handle_user_data(request_keys, expected_keys)

            if not ArchimatchUser.objects.filter(id=data.get("id")).exists():
                raise APIException("cet utilisateur n'existe pas")

            user = ArchimatchUser.objects.get(id=data.get("id"))
            password = data.get("password")
            confirm_password = data.get("confirm_password")

            if password == confirm_password and user.password == "":
                user.set_password(confirm_password)
                user.save()
            else:
                raise APIException("Vous avez déja un mot de passe")

            response_data = {
                "message": "password successfully updated",
                "status_code": status.HTTP_200_OK,
            }
            return Response(
                response_data.get("message"), status=response_data.get("status_code")
            )
        except APIException as e:
            return Response({"message": str(e)}, status=e.status_code)
        except Exception as e:
            return Response({"message": str(e)}, status=status.HTTP_410_GONE)
