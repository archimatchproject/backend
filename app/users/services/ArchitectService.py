"""
Module containing AdminService class.

This module provides service methods for handling admin users, including creation,
updating, decoding tokens, retrieving admin by user ID, retrieving admin by token,
handling user data validation, and admin login authentication.

Classes:
    AdminService: Service class for admin user operations.
"""

from django.utils.translation import get_language_from_request

from rest_framework import serializers
from rest_framework import status
from rest_framework.exceptions import APIException
from rest_framework.exceptions import NotFound
from rest_framework.response import Response

from app.email_templates.signals import api_success_signal
from app.users.models.Architect import Architect
from app.users.serializers.ArchitectSerializer import ArchitectBaseDetailsSerializer
from app.users.serializers.ArchitectSerializer import ArchitectCompanyDetailsSerializer
from app.users.serializers.ArchitectSerializer import ArchitectSerializer
from app.users.serializers.UserAuthSerializer import UserAuthSerializer
from app.users.utils import generate_password_reset_token
from app.users.utils import validate_password_reset_token
from project_core.django import base as settings


class ArchitectService:
    """
    Service class for Architect user operations.

    This class provides methods to handle architect user-related operations such as
    creating architect users, updating architect user data, decoding tokens, retrieving
    architect users by various criteria, handling user data validation, and architect login.
    """

    @classmethod
    def architect_send_reset_password_link(cls, request):
        """
        send reset password link for architect.


        """
        try:
            data = request.data
            serializer = UserAuthSerializer(data=data)
            serializer.is_valid(raise_exception=True)
            email = serializer.validated_data.get("email")

            architect = Architect.objects.get(user__email=email)
            email_images = settings.ARCHITECT_PASSWORD_IMAGES
            token = generate_password_reset_token(architect.user.id)
            language_code = get_language_from_request(request)
            url = f"""{settings.BASE_FRONTEND_URL}/{language_code}"""
            reset_link = f"""{url}/architect/forget-password/{token}"""
            context = {
                "first_name": architect.user.first_name,
                "last_name": architect.user.last_name,
                "email": email,
                "reset_link": reset_link,
            }
            signal_data = {
                "template_name": "architect_reset_password.html",
                "context": context,
                "to_email": email,
                "subject": "Architect Reset Password",
                "images": email_images,
            }
            api_success_signal.send(sender=cls, data=signal_data)
            return Response(
                {"message": "email sent successfully"},
                status=status.HTTP_200_OK,
            )
        except Architect.DoesNotExist:
            raise NotFound(detail="Architect not found")
        except Exception as e:
            raise APIException(
                detail=str(e),
            )

    @classmethod
    def architect_validate_password_token(cls, request):
        """
        validate password token
        """
        try:
            data = request.data
            token = data.get("token", False)
            if not token:
                raise serializers.ValidationError(detail="token is required")

            user_id, error = validate_password_reset_token(token)
            if error:
                raise APIException(detail=error)
            architect = Architect.objects.get(user__id=user_id)
            serializer = ArchitectSerializer(architect)
            return Response(
                serializer.data,
                status=status.HTTP_200_OK,
            )
        except Architect.DoesNotExist:
            raise NotFound(detail="Architect not found")
        except APIException as e:
            raise e
        except Exception as e:
            raise APIException(detail=str(e))

    @classmethod
    def architect_get_profile(cls, request):
        """
        Retrieves architect information.

        Args:
            request (Request): Django request object containing user ID.

        Returns:
            Response: Response object containing architect data.

        Raises:
            APIException: If there are errors during the process.
        """
        user_id = request.user.id
        try:
            architect = Architect.objects.get(user__id=user_id)
            architect_serializer = ArchitectSerializer(architect)
            return Response(
                architect_serializer.data,
                status=status.HTTP_200_OK,
            )
        except Architect.DoesNotExist:
            raise NotFound(detail="Architect not found.", code=status.HTTP_404_NOT_FOUND)
        except APIException as e:
            raise e
        except Exception as e:
            raise APIException(detail=str(e))

    @classmethod
    def architect_update_base_details(cls, request):
        """
        Updates an architect's profile information

        Args:
            request (Request): Django request object containing architect's profile data.

        Returns:
            Response: Response object indicating success or failure of the profile update.

        Raises:
            APIException: If there are errors during architect profile update.
        """
        try:
            data = request.data
            serializer = ArchitectBaseDetailsSerializer(data=data)
            serializer.is_valid(raise_exception=True)
            user_id = request.user.id
            architect = Architect.objects.get(user__id=user_id)
            user = architect.user

            # update user information
            user_fields = ["first_name", "last_name", "email", "phone_number"]
            for field in user_fields:
                if field in data:
                    setattr(user, field, data.pop(field))
            user.save()

            # Update Architect data
            for attr, value in data.items():
                setattr(architect, attr, value)
            architect.save()

            response_data = {
                "message": "Architect successfully updated",
            }
            return Response(
                response_data,
                status=status.HTTP_200_OK,
            )
        except Architect.DoesNotExist:
            raise NotFound(detail="Architect not found.")
        except APIException as e:
            raise e
        except Exception as e:
            raise APIException(detail=str(e))

    @classmethod
    def architect_update_company_details(cls, request):
        """
        Updates an architect's company profile information.

        Args:
            request (Request): Django request object containing architect's company profile data.

        Returns:
            Response: Response object indicating success or failure of the company profile update.

        Raises:
            APIException: If there are errors during architect company profile update.
        """
        try:
            data = request.data
            serializer = ArchitectCompanyDetailsSerializer(data=data)
            serializer.is_valid(raise_exception=True)
            user_id = request.user.id
            architect = Architect.objects.get(user__id=user_id)

            for attr, value in data.items():
                setattr(architect, attr, value)
            architect.save()

            response_data = {
                "message": "Architect successfully updated",
            }
            return Response(
                response_data,
                status=status.HTTP_200_OK,
            )
        except Architect.DoesNotExist:
            raise NotFound(detail="Architect not found.")
        except APIException as e:
            raise e
        except Exception as e:
            raise APIException(detail=str(e))

    @classmethod
    def architect_update_needs(cls, request):
        """
        Updates an architect's needs.

        Args:
            request (Request): Django request object containing architect's needs data.

        Returns:
            Response: Response object indicating success or failure of the needs update.

        Raises:
            APIException: If there are errors during architect needs update.
        """
        try:
            data = request.data
            needs = data.get("needs", [])
            if len(needs) > 0:
                raise serializers.ValidationError(detail="needs are required")
            user_id = request.user.id
            architect = Architect.objects.get(user__id=user_id)
            architect.needs.set(needs)
            architect.save()

            response_data = {
                "message": "Architect successfully updated",
            }
            return Response(
                response_data,
                status=status.HTTP_200_OK,
            )
        except Architect.DoesNotExist:
            raise NotFound(detail="Architect not found.")
        except APIException as e:
            raise e
        except Exception as e:
            raise APIException(detail=str(e))
