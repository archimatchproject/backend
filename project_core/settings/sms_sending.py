"""
Module-level constants for Twilio configuration.
"""

import environ


env = environ.Env()

TWILIO_ACCOUNT_SID = env("TWILIO_ACCOUNT_SID")
TWILIO_AUTH_TOKEN = env("TWILIO_AUTH_TOKEN")
TWILIO_VERIFY_SERVICE_SID = env("TWILIO_VERIFY_SERVICE_SID")
TWILIO_SMS_CHANNEL = "sms"
