from app.users.models import ArchimatchUser
from rest_framework.response import Response
from rest_framework import status
from app.users.services.validation.exceptions import UserDataException
from rest_framework.exceptions import APIException

class ArchimatchUserService:
    
    @classmethod
    def handle_user_data(cls, request_keys, expected_keys):
        if not expected_keys.issubset(request_keys):
            missing_keys = expected_keys - request_keys
            raise UserDataException(f"Missing keys: {', '.join(missing_keys)}")

    @classmethod
    def create_password(cls, request):
        try:
            data = request.data
            request_keys = set(data.keys())
            expected_keys = {'id', 'password', 'confirm_password'}
            
            # Validate input keys
            cls.handle_user_data(request_keys, expected_keys)

            # Check if user exists
            if not ArchimatchUser.objects.filter(id=data.get("id")).exists():
                response_data = {
                    'message': 'User does not exist',
                    'status_code': status.HTTP_404_NOT_FOUND
                }
                return Response(response_data, status=response_data['status_code'])

            user = ArchimatchUser.objects.get(id=data.get("id"))
            password = data.get("password")
            confirm_password = data.get("confirm_password")

            # Set password if conditions are met
            if password == confirm_password and user.password == "":
                user.set_password(confirm_password)
                user.save()
                response_data = {
                    'message': 'Password successfully updated',
                    'status_code': status.HTTP_200_OK
                }
            else:
                response_data = {
                    'message': 'Password already set or passwords do not match',
                    'status_code': status.HTTP_400_BAD_REQUEST
                }

            return Response(response_data['message'], status=response_data['status_code'])

        except UserDataException as e:
            return Response({"message": str(e)}, status=status.HTTP_400_BAD_REQUEST)

        except APIException as e:
            return Response({"message": str(e)}, status=e.status_code)
        
    @classmethod
    def reset_password(cls, request):
        try:
            data = request.data
            request_keys = set(data.keys())
            expected_keys = {'id', 'old_password', 'new_password', 'confirm_new_password'}
            
            # Validate input keys
            cls.handle_user_data(request_keys, expected_keys)

            # Check if user exists
            if not ArchimatchUser.objects.filter(id=data.get("id")).exists():
                response_data = {
                    'message': {'message':'User does not exist'},
                    'status_code': status.HTTP_404_NOT_FOUND
                }
                return Response(response_data['message'], status=response_data['status_code'])

            user = ArchimatchUser.objects.get(id=data.get("id"))
            old_password = data.get("old_password")
            new_password = data.get("new_password")
            confirm_new_password = data.get("confirm_new_password")

            # Check if old password matches
            if not user.check_password(old_password):
                response_data = {
                    'message': {'message':'Incorrect old password'},
                    'status_code': status.HTTP_400_BAD_REQUEST
                }
                return Response(response_data['message'], status=response_data['status_code'])

            # Set new password if conditions are met
            if new_password == confirm_new_password:
                user.set_password(new_password)
                user.save()
                response_data = {
                    'message': {'message':'Password successfully updated'},
                    'status_code': status.HTTP_200_OK
                }
            else:
                response_data = {
                    'message': {'message':'New passwords do not match'},
                    'status_code': status.HTTP_400_BAD_REQUEST
                }

            return Response(response_data['message'], status=response_data['status_code'])

        except UserDataException as e:
            return Response({"message": str(e)}, status=status.HTTP_400_BAD_REQUEST)

        except APIException as e:
            return Response({"message": str(e)}, status=e.status_code)
