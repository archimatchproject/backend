"""
Module: SMSVerificationService

This module defines the SMSVerificationService class that handles  Verify
operations such as sending verification codes and checking verification codes.

Classes:
    SMSService: A Generuc service class for Verify operations.

"""

from app.core.services.SMS.SMSService import SMSService


class SMSVerificationService:
    """
    A generic verification service that utilizes an SMS service provider for sending
    and verifying SMS codes.

    Attributes:
        sms_service (SMSService): An instance of a class that implements the SMSService
         interface.
    """

    def __init__(self, sms_service: SMSService):
        """
        Initializes the SMSVerificationService with a specific SMS service provider.

        Args:
            sms_service (SMSService): An instance of a class that implements the SMSService
            interface.
        """
        self.sms_service = sms_service

    def send_verification_code(self, phone):
        """
        Sends a verification code to the specified phone number using the configured SMS
        service provider.

        Args:
            phone (str): The phone number to which the verification code is sent.

        Returns:
            str: The verification SID if successful, otherwise an error message.
        """
        return self.sms_service.send_verification_code(phone)

    def check_verification_code(self, phone, code):
        """
        Checks the verification code for the specified phone number using the configured
        SMS service provider.

        Args:
            phone (str): The phone number to be verified.
            code (str): The verification code to be checked.

        Returns:
            bool: True if the verification code is approved, otherwise False.
        """
        return self.sms_service.check_verification_code(phone, code)
