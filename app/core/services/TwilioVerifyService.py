"""
Module: Twilio Verify Service

This module defines the TwilioVerifyService class that handles Twilio Verify
operations such as sending verification codes and checking verification codes.

Classes:
    TwilioVerifyService: A service class for Twilio Verify operations.

"""

from django.conf import settings

from twilio.base.exceptions import TwilioRestException
from twilio.rest import Client


class TwilioVerifyService:
    """
    A service class for handling Twilio Verify operations such as sending
    verification codes and checking verification codes.

    Attributes:
        client (Client): The Twilio Client initialized with account SID and auth token.
        verify (Verify): The Twilio Verify service initialized with the service SID.
    """

    client = Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)
    verify = client.verify.services(settings.TWILIO_VERIFY_SERVICE_SID)

    @classmethod
    def send_verification_code(cls, phone):
        """
        Sends a verification code to the specified phone number via SMS.

        Args:
            phone (str): The phone number to which the verification code is sent.

        Returns:
            str: The verification SID if successful, otherwise an error message.
        """
        try:
            verification = cls.verify.verifications.create(to=phone, channel="sms")
            print(verification.sid)
            return verification.sid
        except TwilioRestException as e:
            return str(e)

    @classmethod
    def check_verification_code(cls, phone, code):
        """
        Checks the verification code for the specified phone number.

        Args:
            phone (str): The phone number to be verified.
            code (str): The verification code to be checked.

        Returns:
            bool: True if the verification code is approved, otherwise False.
        """
        try:
            result = cls.verify.verification_checks.create(to=phone, code=code)
            if result.status == "approved":
                return True
            else:
                return False
        except TwilioRestException as e:
            return False
