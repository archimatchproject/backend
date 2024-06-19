from rest_framework import status

# from app.users.exceptions import UserDataException
from rest_framework.exceptions import APIException
from rest_framework.response import Response

from app.users.models import ArchimatchUser, Supplier
from app.users.models.utils.SocialMedia import SocialMedia
from app.users.serializers import SupplierSerializer


class SupplierService:
    serializer_class = SupplierSerializer

    @classmethod
    def handle_user_data(self, request_keys, expected_keys):
        if not expected_keys.issubset(request_keys):
            missing_keys = expected_keys - request_keys
            raise APIException(f"Missing keys:".join(missing_keys))

    @classmethod
    def supplier_signup(cls, request):
        try:
            data = request.data
            request_keys = set(data.keys())
            expected_keys = {"email"}
            cls.handle_user_data(request_keys, expected_keys)

            email = data.get("email")

            if not Supplier.objects.filter(user__email=email).exists():
                user = ArchimatchUser.objects.create(email=email, username=email)
                supplier = Supplier.objects.create(user=user)
                user.save()
                supplier.save()

                response_data = {
                    "message": "Supplier_Created",
                    "status_code": status.HTTP_201_CREATED,
                }
            else:
                response_data = {
                    "message": "Supplier_Exists",
                    "status_code": status.HTTP_401_UNAUTHORIZED,
                }

            return Response(
                response_data.get("message"), status=response_data.get("status_code")
            )
        except APIException as e:
            return Response({"message": str(e)}, status=e.status_code)
        except Exception as e:
            return Response({"message": str(e)}, status=status.HTTP_410_GONE)

    @classmethod
    def supplier_login(cls, request):
        try:
            data = request.data
            request_keys = set(data.keys())
            expected_keys = {"email"}
            cls.handle_user_data(request_keys, expected_keys)

            email = data.get("email")

            if Supplier.objects.filter(user__email=email).exists():
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
                    "message": "Supplier Not Found",
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
    def supplier_first_connection(self, request):
        try:

            data = request.data
            request_keys = set(data.keys())
            expected_keys = {
                "type",
                "company_name",
                "address",
                "phone_number",
                "speciality",
                "id",
            }
            SupplierService.handle_user_data(request_keys, expected_keys)

            if not Supplier.objects.filter(id=data.get("id")).exists():
                raise APIException("ce fournisseur n'existe pas")

            supplier = Supplier.objects.get(id=data.get("id"))
            phone_number = data.pop("phone_number")
            # update user data
            user = supplier.user
            user.phone_number = phone_number
            user.save()

            Supplier.objects.filter(id=data.get("id")).update(**data)

            response_data = {
                "message": "Supplier successfully updated",
                "status_code": status.HTTP_200_OK,
            }
            return Response(
                response_data.get("message"), status=response_data.get("status_code")
            )
        except APIException as e:
            return Response({"message": str(e)}, status=e.status_code)
        except Exception as e:
            return Response({"message": str(e)}, status=status.HTTP_410_GONE)

    @classmethod
    def supplier_update_profile(self, request):
        try:

            data = request.data
            request_keys = set(data.keys())
            expected_keys = {
                "company_name",
                "address",
                "phone_number",
                "speciality",
                "id",
            }
            SupplierService.handle_user_data(request_keys, expected_keys)

            if not Supplier.objects.filter(id=data.get("id")).exists():
                raise APIException("ce fournisseur n'existe pas")

            supplier = Supplier.objects.get(id=data.get("id"))
            phone_number = data.pop("phone_number")
            # update user data
            user = supplier.user
            user.phone_number = phone_number
            user.save()

            Supplier.objects.filter(id=data.get("id")).update(**data)

            response_data = {
                "message": "Supplier successfully updated",
                "status_code": status.HTTP_200_OK,
            }
            return Response(
                response_data.get("message"), status=response_data.get("status_code")
            )
        except APIException as e:
            return Response({"message": str(e)}, status=e.status_code)
        except Exception as e:
            return Response({"message": str(e)}, status=status.HTTP_410_GONE)

    @classmethod
    def supplier_update_general_settings(self, request):
        try:

            data = request.data
            request_keys = set(data.keys())
            expected_keys = {"bio", "id"}
            SupplierService.handle_user_data(request_keys, expected_keys)

            if not Supplier.objects.filter(id=data.get("id")).exists():
                raise APIException("ce fournisseur n'existe pas")

            Supplier.objects.filter(id=data.get("id")).update(**data)

            response_data = {
                "message": "Supplier successfully updated",
                "status_code": status.HTTP_200_OK,
            }
            return Response(
                response_data.get("message"), status=response_data.get("status_code")
            )
        except APIException as e:
            return Response({"message": str(e)}, status=e.status_code)
        except Exception as e:
            return Response({"message": str(e)}, status=status.HTTP_410_GONE)

    @classmethod
    def supplier_update_links(self, request):
        try:

            data = request.data
            request_keys = set(data.keys())
            expected_keys = {"facebook", "instagram", "website", "id"}
            SupplierService.handle_user_data(request_keys, expected_keys)

            if not Supplier.objects.filter(id=data.get("id")).exists():
                raise APIException("ce fournisseur n'existe pas")

            supplier = Supplier.objects.get(id=data.get("id"))
            data.pop("id")
            if not supplier.social_links:
                supplier.social_links = (
                    supplier.social_links
                ) = SocialMedia.objects.create(**data)
                supplier.save()

            else:
                social_links = supplier.social_links
                supplier.social_links = SocialMedia.objects.filter(
                    id=social_links.id
                ).update(**data)
                supplier.save()

            response_data = {
                "message": "Supplier successfully updated",
                "status_code": status.HTTP_200_OK,
            }
            return Response(
                response_data.get("message"), status=response_data.get("status_code")
            )
        except APIException as e:
            return Response({"message": str(e)}, status=e.status_code)
        except Exception as e:
            return Response({"message": str(e)}, status=status.HTTP_410_GONE)
