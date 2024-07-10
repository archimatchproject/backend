"""
Module: Client Service

This module defines the ClientService class that handles client-related operations such as login
 using email or phone number.

Classes:
    ClientService: Service class for client-related operations.

"""

from rest_framework import serializers
from rest_framework import status
from rest_framework.exceptions import APIException
from rest_framework.exceptions import NotFound
from rest_framework.response import Response

from app.core.services.SMS.SMSVerificationService import SMSVerificationService
from app.core.services.SMS.TwilioVerifyService import TwilioVerifyService
from app.core.validation.exceptions import InvalidPhoneNumberException
from app.core.validation.exceptions import SMSException
from app.core.validation.validate_data import is_valid_phone_number
from app.email_templates.signals import api_success_signal
from app.users.models.ArchimatchUser import ArchimatchUser
from app.users.models.Client import Client
from app.users.serializers.ClientSerializer import ClientSerializer
from app.users.serializers.UserAuthSerializer import UserAuthSerializer
from app.users.utils import generate_password_reset_token
from app.users.utils import validate_password_reset_token
from project_core.django import base as settings


class ClientService:
    """
    Service class for handling client-related operations such as login using email or phone number.

    """

    twilio_service = TwilioVerifyService()
    sms_verification_service = SMSVerificationService(twilio_service)

    @classmethod
    def client_login_email(cls, request):
        """
        Authenticates a client using email and checks if they have set a password.

        Args:
            request (Request): Django request object containing client's email.

        Returns:
            Response: Response object with a message indicating if the client has set a password.

        Raises:
            serializers.ValidationError: If there are errors during client authentication.
        """
        try:
            data = request.data
            email_req = data.get("email", None)
            if email_req is None:
                raise serializers.ValidationError(detail="Email is required")
            if not Client.objects.filter(user__email=email_req).exists():
                raise NotFound(detail="Client Not Found")

            user = ArchimatchUser.objects.get(email=email_req)
            has_password = user.password != ""
            response_data = {"has_password": has_password}

            return Response(
                response_data,
                status=status.HTTP_200_OK,
            )

        except APIException as e:
            raise e
        except Exception as e:
            raise APIException(detail=str(e))

    @classmethod
    def client_send_verification_code(cls, request):
        """
        Sends a verification code to the client's phone number.

        Args:
            request (Request): Django request object containing client's phone number.

        Returns:
            Response: Response object indicating whether the verification code was
            sent successfully.
        """
        try:
            data = request.data
            phone_number = data.get("phone_number")
            if phone_number is None:
                raise serializers.ValidationError(detail="phone number is required")
            is_valid_phone_number(phone_number)
            if not Client.objects.filter(user__phone_number=phone_number).exists():
                raise NotFound(detail="Client not found")

            sid = cls.sms_verification_service.send_verification_code(phone_number)
            if not sid:
                raise serializers.ValidationError(detail="Failed to send verification code.")

            return Response(
                {"message": "Verification code sent successfully."},
                status=status.HTTP_200_OK,
            )

        except SMSException:
            raise serializers.ValidationError(detail="Error Sending SMS Code")
        except InvalidPhoneNumberException as e:
            raise serializers.ValidationError(detail=str(e))
        except APIException as e:
            raise e
        except Exception as e:
            raise APIException(detail=str(e))

    @classmethod
    def client_verify_verification_code(cls, request):
        """
        Authenticates a client using phone number and verifies the SMS code.

        Args:
            request (Request): Django request object containing client's phone number and
            verification code.

        Returns:
            Response: Response object with a message indicating if the client has set a password
            and their email.
        """
        try:
            data = request.data
            phone_number = data.get("phone_number", None)
            verification_code = data.get("verification_code", None)
            if verification_code is None or phone_number is None:
                raise serializers.ValidationError(
                    detail="verification code and phone number are required"
                )

            if not Client.objects.filter(user__phone_number=phone_number).exists():
                raise NotFound(detail="Client Not Found")

            user = ArchimatchUser.objects.get(phone_number=phone_number)

            # Verify the SMS code
            if not cls.sms_verification_service.check_verification_code(
                phone_number,
                verification_code,
            ):
                raise serializers.ValidationError(detail="Invalid verification code")

            # Determine response data based on whether user has set a password
            if user.password == "":
                response_data = {
                    "message": {
                        "has_password": False,
                        "email": user.username,
                    },
                }
            else:
                response_data = {
                    "message": {"has_password": True, "email": user.email},
                }

            return Response(
                response_data.get("message"),
                status=status.HTTP_200_OK,
            )

        except SMSException:
            raise serializers.ValidationError(detail="Error Verifying SMS Code")
        except APIException as e:
            raise e
        except Exception as e:
            raise APIException(detail=str(e))

    @classmethod
    def client_send_reset_password_link(cls, request):
        """
        send reset password link for clients.


        """
        try:
            data = request.data
            serializer = UserAuthSerializer(data=data)
            serializer.is_valid(raise_exception=True)
            email = serializer.validated_data.get("email")

            client = Client.objects.get(user__email=email)
            token = generate_password_reset_token(client.user.id)
            email_images = settings.CLIENT_PASSWORD_IMAGES
            context = {
                "first_name": client.user.first_name,
                "last_name": client.user.last_name,
                "email": email,
                "reset_link": f"http://localhost:8000/fr/client/reset_password/{str(token)}",
            }
            signal_data = {
                "template_name": "client_reset_password.html",
                "context": context,
                "to_email": email,
                "subject": "client Reset Password",
                "images": email_images,
            }
            api_success_signal.send(sender=cls, data=signal_data)
            return Response(
                {"message": "email sent successfully"},
                status=status.HTTP_200_OK,
            )
        except Client.DoesNotExist:
            raise NotFound(detail="Client not found")
        except Exception as e:
            raise APIException(
                detail=str(e),
            )

    @classmethod
    def client_validate_password_token(cls, request):
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
            print("aaaaaaaaaaaaaa", user_id)
            client = Client.objects.get(user__id=user_id)
            serializer = ClientSerializer(client)
            return Response(
                serializer.data,
                status=status.HTTP_200_OK,
            )
        except Client.DoesNotExist:
            raise NotFound(detail="Client not found")
        except APIException as e:
            raise e
        except Exception as e:
            raise APIException(
                detail=str(e),
            )
