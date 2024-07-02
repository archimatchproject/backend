"""
Module: SMSService

This module defines the SMSService class that handles  Verify
operations such as sending verification codes and checking verification codes.

Classes:
    SMSService: An abstract service class for Verify operations.

"""

from abc import ABC
from abc import abstractmethod


class SMSService(ABC):
    """
    An  Abstract SMSService that utilizes an SMS service provider for sending
    and verifying SMS codes.
    """

    @abstractmethod
    def send_verification_code(self, phone):
        """
        Sends a verification code to the specified phone number via SMS.

        Args:
            phone (str): The phone number to which the verification code is sent.

        Returns:
            str: The verification SID if successful, otherwise an error message.
        """
        pass

    @abstractmethod
    def check_verification_code(self, phone, code):
        """
        Checks the verification code for the specified phone number.

        Args:
            phone (str): The phone number to be verified.
            code (str): The verification code to be checked.

        Returns:
            bool: True if the verification code is approved, otherwise False.
        """
        pass
