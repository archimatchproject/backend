"""
Module-level constants for Twilio configuration.
"""

from project_core.env import env


TWILIO_ACCOUNT_SID = env("TWILIO_ACCOUNT_SID")
TWILIO_AUTH_TOKEN = env("TWILIO_AUTH_TOKEN")
TWILIO_VERIFY_SERVICE_SID = env("TWILIO_VERIFY_SERVICE_SID")
TWILIO_SMS_CHANNEL = "sms"
