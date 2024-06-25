"""
Module for defining a custom API exception class for user data-related errors.

This module provides the `UserDataException` class, which extends `APIException`
from Django REST Framework. It handles exceptions related to user data operations.

"""

from rest_framework import status
from rest_framework.exceptions import APIException


class UserDataException(APIException):
    """
    Custom exception class for user data-related errors.
    """

    def __init__(self, detail=None, status_code=None):
        """
        Initialize the exception with custom detail and status code.

        Args:
            detail (str): Detail message for the exception. Defaults to default_detail if not provided.
            status_code (int): HTTP status code for the exception. Defaults to default_status_code if not provided.
        """
        self.detail = detail or self.default_detail
        self.status_code = status_code or self.default_status_code

    default_detail = "A custom API exception occurred."
    default_status_code = status.HTTP_400_BAD_REQUEST


class InvalidPhoneNumberException(Exception):
    """
    Custom exception class for phone number validation errors.
    """

    pass


class SMSException(Exception):
    """
    Custom exception class for sms-related errors.
    """

    pass
