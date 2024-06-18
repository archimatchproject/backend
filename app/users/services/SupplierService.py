from app.users.models import Supplier, ArchimatchUser
from app.users.serializers import SupplierSerializer
from rest_framework.response import Response
from rest_framework import status
from app.users.services.validation.exceptions import UserDataException
from rest_framework.exceptions import APIException
from app.users.models.utils.SocialMedia import SocialMedia
class SupplierService:
    serializer_class = SupplierSerializer

    @classmethod
    def handle_user_data(cls, request_keys, expected_keys):
        if not expected_keys.issubset(request_keys):
            missing_keys = expected_keys - request_keys
            raise UserDataException(f"Missing keys: {', '.join(missing_keys)}")

    @classmethod
    def signup(cls, request):
        try:
            data = request.data
            request_keys = set(data.keys())
            expected_keys = {'email'}
            cls.handle_user_data(request_keys, expected_keys)

            email = data.get("email")

            if not Supplier.objects.filter(user__email=email).exists():
                if not ArchimatchUser.objects.filter(email=email).exists():
                    user = ArchimatchUser.objects.create(email=email, username=email,user_type='Supplier')
                    supplier = Supplier.objects.create(user=user)
                    response_data = {
                        'message': {'message': 'supplier_created'},
                        'status_code': status.HTTP_201_CREATED
                    }
                else:
                    response_data = {
                        'message': {'message': 'user_exists'},
                        'status_code': status.HTTP_400_BAD_REQUEST
                    }
            else:
                response_data = {
                    'message': {'message': 'supplier_exists'},
                    'status_code': status.HTTP_400_BAD_REQUEST
                }

            return Response(response_data.get("message"), status=response_data.get("status_code"))

        except UserDataException as e:
            return Response({"message": str(e)}, status=status.HTTP_400_BAD_REQUEST)

        except APIException as e:
            return Response({"message": str(e)}, status=e.status_code)

    @classmethod
    def login(cls, request):
        try:
            data = request.data
            request_keys = set(data.keys())
            expected_keys = {'email'}
            cls.handle_user_data(request_keys, expected_keys)

            email = data.get("email")

            if Supplier.objects.filter(user__email=email).exists():
                user = ArchimatchUser.objects.get(username=email)
                if user.password == "":
                    response_data = {
                        'message': {'has_password': False, 'id': user.id},
                        'status_code': status.HTTP_200_OK
                    }
                else:
                    response_data = {
                        'message': {'has_password': True},
                        'status_code': status.HTTP_200_OK
                    }
            else:
                response_data = {
                    'message': {'message': 'supplier_not_found'},
                    'status_code': status.HTTP_404_NOT_FOUND
                }

            return Response(response_data.get("message"), status=response_data.get("status_code"))

        except UserDataException as e:
            return Response({"message": str(e)}, status=status.HTTP_400_BAD_REQUEST)

        except APIException as e:
            return Response({"message": str(e)}, status=e.status_code)

    @classmethod
    def first_connection(cls, request):
        try:
            data = request.data
            request_keys = set(data.keys())
            expected_keys = {'company_address', 'company_speciality', 'company_name', 'phone_number', 'speciality_type', 'id', 'appearance'}
            cls.handle_user_data(request_keys, expected_keys)

            if not Supplier.objects.filter(id=data.get("id")).exists():
                response_data = {
                    'message': {'message':'supplier doesn\'t exist'},
                    'status_code': status.HTTP_404_NOT_FOUND
                }
                return Response(response_data.get("message"), status=response_data.get("status_code"))

            supplier = Supplier.objects.get(id=data.get("id"))
            phone_number = data.pop("phone_number")

            # Update user data
            user = supplier.user
            user.phone_number = phone_number
            user.save()

            # Update supplier data
            speciality_type_ids = data.pop("speciality_type")
            supplier.speciality_type.set(speciality_type_ids)

            Supplier.objects.filter(id=data.get("id")).update(**data)

            response_data = {
                'message': {'message':'supplier successfully updated'},
                'status_code': status.HTTP_200_OK
            }
            return Response(response_data.get("message"), status=response_data.get("status_code"))

        except UserDataException as e:
            return Response({"message": str(e)}, status=status.HTTP_400_BAD_REQUEST)

        except APIException as e:
            return Response({"message": str(e)}, status=e.status_code)
      
    @classmethod
    def update_profile(cls, request):
        try:
            data = request.data
            request_keys = set(data.keys())
            expected_keys = {'company_name', 'company_address', 'phone_number', 'company_speciality', 'id'}
            cls.handle_user_data(request_keys, expected_keys)

            if not Supplier.objects.filter(id=data.get("id")).exists():
                response_data = {
                    'message': {'message': 'supplier doesn\'t exist'},
                    'status_code': status.HTTP_404_NOT_FOUND
                }
                return Response(response_data.get("message"), status=response_data.get("status_code"))

            supplier = Supplier.objects.get(id=data.get("id"))
            phone_number = data.pop("phone_number")

            # Update user data
            user = supplier.user
            user.phone_number = phone_number
            user.save()

            # Update supplier data
            Supplier.objects.filter(id=data.get("id")).update(**data)

            response_data = {
                'message': {'message': 'supplier successfully updated'},
                'status_code': status.HTTP_200_OK
            }
            return Response(response_data.get("message"), status=response_data.get("status_code"))

        except UserDataException as e:
            return Response({"message": str(e)}, status=status.HTTP_400_BAD_REQUEST)

        except APIException as e:
            return Response({"message": str(e)}, status=e.status_code)

    

    @classmethod
    def update_bio(cls, request):
        try:
            data = request.data
            request_keys = set(data.keys())
            expected_keys = {'bio', 'id'}
            cls.handle_user_data(request_keys, expected_keys)

            if not Supplier.objects.filter(id=data.get("id")).exists():
                response_data = {
                    'message': {'message': "Supplier doesn't exist"},
                    'status_code': status.HTTP_404_NOT_FOUND
                }
                return Response(response_data.get("message"), status=response_data.get("status_code"))

            Supplier.objects.filter(id=data.get("id")).update(bio=data.get('bio'))

            response_data = {
                'message': {'message': 'Supplier bio successfully updated'},
                'status_code': status.HTTP_200_OK
            }
            return Response(response_data.get("message"), status=response_data.get("status_code"))

        except UserDataException as e:
            return Response({"message": str(e)}, status=status.HTTP_400_BAD_REQUEST)

        except APIException as e:
            return Response({"message": str(e)}, status=e.status_code)
    
    @classmethod
    def update_presentation_video(cls, request):
        try:
            data = request.data
            request_keys = set(data.keys())
            expected_keys = {'presentation_video', 'id'}
            cls.handle_user_data(request_keys, expected_keys)

            if not Supplier.objects.filter(id=data.get("id")).exists():
                response_data = {
                    'message': {'message': "Supplier doesn't exist"},
                    'status_code': status.HTTP_404_NOT_FOUND
                }
                return Response(response_data.get("message"), status=response_data.get("status_code"))

            Supplier.objects.filter(id=data.get("id")).update(presentation_video=data.get('presentation_video'))

            response_data = {
                'message': {'message': 'Supplier presentation video successfully updated'},
                'status_code': status.HTTP_200_OK
            }
            return Response(response_data.get("message"), status=response_data.get("status_code"))

        except UserDataException as e:
            return Response({"message": str(e)}, status=status.HTTP_400_BAD_REQUEST)

        except APIException as e:
            return Response({"message": str(e)}, status=e.status_code)
    
    @classmethod
    def update_links(cls, request):
        try:
            data = request.data
            request_keys = set(data.keys())
            expected_keys = {'facebook', 'instagram', 'website', 'id'}
            cls.handle_user_data(request_keys, expected_keys)

            if not Supplier.objects.filter(id=data.get("id")).exists():
                response_data = {
                    'message': {'message': "Supplier doesn't exist"},
                    'status_code': status.HTTP_404_NOT_FOUND
                }
                return Response(response_data.get("message"), status=response_data.get("status_code"))

            supplier = Supplier.objects.get(id=data.get("id"))
            social_links_data = {
                'facebook': data.get('facebook'),
                'instagram': data.get('instagram'),
                'website': data.get('website')
            }

            if not supplier.social_links:
                social_links = SocialMedia.objects.create(**social_links_data)
                supplier.social_links = social_links
                supplier.save()
            else:
                social_links = supplier.social_links
                SocialMedia.objects.filter(id=social_links.id).update(**social_links_data)
                supplier.refresh_from_db()

            response_data = {
                'message': {'message': 'Supplier social links successfully updated'},
                'status_code': status.HTTP_200_OK
            }
            return Response(response_data.get("message"), status=response_data.get("status_code"))

        except UserDataException as e:
            return Response({"message": str(e)}, status=status.HTTP_400_BAD_REQUEST)

        except APIException as e:
            return Response({"message": str(e)}, status=e.status_code)