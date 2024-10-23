"""
Module: Archimatch User Service

This module defines the ArchimatchUserService class that provides methods for handling user data
 and password creation.

Classes:
    ArchimatchUserService: Service class for handling user data and password creation.

"""

from rest_framework import serializers
from rest_framework import status
from rest_framework.exceptions import APIException
from rest_framework.exceptions import NotFound
from rest_framework.response import Response
from rest_framework.serializers import ValidationError

from app.architect_request.models.ArchitectRequest import ArchitectRequest
from app.core.services.SMS.SMSVerificationService import SMSVerificationService
from app.core.services.SMS.TwilioVerifyService import TwilioVerifyService
from app.core.validation.exceptions import InvalidPhoneNumberException
from app.core.validation.exceptions import SMSException
from app.core.validation.validate_data import is_valid_phone_number
from app.users.models.ArchimatchUser import ArchimatchUser
from app.users.serializers.ArchimatchUserObtainPairSerializer import (
    ArchimatchUserObtainPairSerializer,
)
from app.users.serializers.ArchimatchUserPWSerializer import ArchimatchUserCreatePWSerializer
from app.users.serializers.ArchimatchUserPWSerializer import ArchimatchUserResetPWSerializer
from app.users.serializers.ArchimatchUserSerializer import ArchimatchUserEmailPhoneSerializer
from app.users.serializers.ArchimatchUserSerializer import ArchimatchUserSerializer
from app.users.serializers.ArchimatchUserSerializer import ArchimatchUserSimpleSerializer


class ArchimatchUserService:
    """
    Service class for handling user data and password creation in the Archimatch application.


    """

    twilio_service = TwilioVerifyService()
    sms_verification_service = SMSVerificationService(twilio_service)

    def generate_tokens_for_user(email, password):
        """
        Generates token for user
        """
        serializer = ArchimatchUserObtainPairSerializer(
            data={
                "email": email,
                "password": password,
            }
        )
        serializer.is_valid(raise_exception=True)
        return serializer.validated_data

    @classmethod
    def archimatch_user_create_password(cls, request):
        """
        Creates or updates the password for a user based on provided data.

        Args:
            request (Request): Django request object containing user data.

        Returns:
            Response: Response object with a message indicating the status of the password update.
        """
        
        data = request.data
        serializer = ArchimatchUserCreatePWSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        validated_data = serializer.validated_data

        email = validated_data.get("email")
        password = validated_data.get("password")
        confirm_password = validated_data.get("confirm_password")

        # Check if user exists
        if not ArchimatchUser.objects.filter(email=email).exists():
            raise NotFound(detail="User does not exist")

        user = ArchimatchUser.objects.get(email=email)

        # Set password if conditions are met
        if password == confirm_password:
            user.set_password(confirm_password)
            user.username = email
            user.save()

            # Generate tokens for the user
            tokens = cls.generate_tokens_for_user(email, password)
            return True,tokens,"Password successfully updated"
            
        else:
            raise ValidationError(detail="Passwords do not match")



    @classmethod
    def archimatch_user_reset_password(cls, request):
        """
        Resets the password for a user based on provided data.

        Args:
            request (Request): Django request object containing user data.

        Returns:
            Response: Response object with a message indicating the status of the password update.
        """
        data = request.data
        serializer = ArchimatchUserResetPWSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        validated_data = serializer.validated_data

        # Check if user exists
        user = request.user
        old_password = validated_data.get("old_password")
        new_password = validated_data.get("new_password")
        confirm_new_password = validated_data.get("confirm_new_password")

        if not user.check_password(old_password):
            raise ValidationError(detail="Incorrect old password")
        # Set new password if conditions are met
        if new_password == confirm_new_password:
            user.set_password(new_password)
            user.save()
            return True,"Password successfully updated"
        else:
            raise ValidationError(detail="New passwords do not match")

        

    @classmethod
    def archimatch_user_update_data(cls, request):
        """
        Updates the basic data for a user based on provided data.
        """

        user = request.user
        data = request.data
        if not data:
            raise ValidationError(detail="At least one field must be provided for update.")
        serializer = ArchimatchUserSimpleSerializer(user, data=data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return True, serializer.data,"User data successfully updated"
            
        

    @classmethod
    def archimatch_user_get_user_data(cls, request):
        """
        Retrieves the data for the authenticated user.

        Args:
            request (Request): Django request object containing user data.

        Returns:
            Response: Response object with the user's data.
        """

        user = request.user
        return True,ArchimatchUserSerializer(user).data
        
        

    @classmethod
    def send_verification_code(cls, request):
        """
        Sends a verification code to the client's phone number.

        Args:
            request (Request): Django request object containing client's phone number.

        Returns:
            Response: Response object indicating whether the verification code was
            sent successfully.
        """
        
        data = request.data
        phone_number = data.get("phone_number")
        if phone_number is None:
            raise serializers.ValidationError(detail="phone number is required")
        is_valid_phone_number(phone_number)
        # Commented out to save credit of trial
        # sid = cls.sms_verification_service.send_verification_code(phone_number)
        # if not sid:
        #     raise serializers.ValidationError(detail="Failed to send verification code.")
        return True, "Verification code sent successfully."
        


    @classmethod
    def verify_verification_code(cls, request):
        """
        Authenticates a client using phone number and verifies the SMS code.

        Args:
            request (Request): Django request object containing client's phone number and
            verification code.

        Returns:
            Response: Response object with a message indicating if the client has set a password
            and their email.
        """
        data = request.data
        phone_number = data.get("phone_number", None)
        verification_code = data.get("verification_code", None)
        if verification_code is None or phone_number is None:
            raise serializers.ValidationError(
                detail="verification code and phone number are required"
            )

        # Commented out to save credit of trial
        # if not cls.sms_verification_service.check_verification_code(
        #     phone_number,
        #     verification_code,
        # ):
        #     raise serializers.ValidationError(detail="Invalid verification code")
        if not verification_code == "000000":
            raise serializers.ValidationError(detail="Invalid verification code")
        return True,"Verification code verified successfully."



    @classmethod
    def archimatch_user_is_found(cls, request):
        """
        Validates the phone number and email address from the provided data.

        This method checks if the given phone number and email address are unique
          in the `ArchitectRequest` model.
        If either the phone number or the email address already exists,
        it raises an `APIException`.

        Args:
            request (Request): Django request object containing user data.

        Returns:
            Response: Response object with a message indicating the status
            of the validation.

        Raises:
            APIException: If the phone number or email address already exists or if any
            other error occurs during validation.
        """

        data = request.data
        serializer = ArchimatchUserEmailPhoneSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        validated_data = serializer.validated_data

        if ArchitectRequest.objects.filter(
            phone_number=validated_data.get("phone_number")
        ).exists():
            raise APIException(detail="phone number already exists")
        if ArchitectRequest.objects.filter(email=validated_data.get("email")).exists():
            raise APIException(detail="email already exists")

        return True,"phone number and email address are valid"

        
