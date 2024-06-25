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

from app.core.services.SMS.SMSService import SMSService
from app.core.validation.exceptions import SMSException


class TwilioVerifyService(SMSService):
    """
    A service class for handling Twilio Verify operations such as sending
    verification codes and checking verification codes.

    Attributes:
        client (Client): The Twilio Client initialized with account SID and auth token.
        verify_service_sid (str): The SID for the Twilio Verify service.
    """

    def __init__(self, client=None, verify_service_sid=None):
        """
        Initializes the TwilioVerifyService with the given client and verify service SID.

        Args:
            client (Client, optional): The Twilio Client. If not provided, it is initialized with settings.
            verify_service_sid (str, optional): The SID for the Twilio Verify service. If not provided, it is taken from settings.
        """
        self.client = client or Client(
            settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN
        )
        self.verify_service_sid = (
            verify_service_sid or settings.TWILIO_VERIFY_SERVICE_SID
        )
        self.verify = self.client.verify.services(self.verify_service_sid)
        self.channel = "sms"

    def send_verification_code(self, phone):
        """
        Sends a verification code to the specified phone number via SMS.

        Args:
            phone (str): The phone number to which the verification code is sent.

        Returns:
            str: The verification SID if successful, otherwise an error message.
        """
        try:
            verification = self.verify.verifications.create(
                to=phone, channel=self.channel
            )
            return verification.sid
        except TwilioRestException as e:
            raise SMSException(f"Error sending verification code: {e.msg}")

    def check_verification_code(self, phone, code):
        """
        Checks the verification code for the specified phone number.

        Args:
            phone (str): The phone number to be verified.
            code (str): The verification code to be checked.

        Returns:
            bool: True if the verification code is approved, otherwise False.
        """
        try:
            result = self.verify.verification_checks.create(to=phone, code=code)
            return result.status == "approved"
        except TwilioRestException as e:
            raise SMSException(f"Error receiving verification code: {e.msg}")
