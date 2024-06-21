"""
Module containing UserAuthSerializer and UserAuthPhoneSerializer classes.

This module provides serializers for user authentication information.

Classes:
    UserAuthSerializer: Serializer for authentication via email.
    UserAuthPhoneSerializer: Serializer for authentication via phone number.
"""

from rest_framework import serializers


class UserAuthSerializer(serializers.Serializer):
    """
    Serializer for authentication via email.

    This serializer validates and serializes the email field for user authentication.

    Fields:
        email: EmailField for user authentication.
    """

    email = serializers.EmailField()


class UserAuthPhoneSerializer(serializers.Serializer):
    """
    Serializer for authentication via phone number.

    This serializer validates and serializes the phone_number field for user authentication.

    Fields:
        phone_number: CharField for user authentication via phone number.
    """

    phone_number = serializers.CharField()


class VerifyCodeSerializer(serializers.Serializer):
    """
    Serializer for verifying the verification code sent to the client's phone number.

    Fields:
        phone_number (str): The phone number of the client, including country code.
        verification_code (str): The verification code sent to the client's phone number.
    """

    phone_number = serializers.CharField()
    verification_code = serializers.CharField()
