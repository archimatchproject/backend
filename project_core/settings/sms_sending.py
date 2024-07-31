"""
Module-level constants for Twilio configuration.
"""

import os

import environ


env = environ.Env()
env.read_env(os.path.join(os.path.dirname(__file__), ".env"))

TWILIO_ACCOUNT_SID = env("TWILIO_ACCOUNT_SID")
TWILIO_AUTH_TOKEN = env("TWILIO_AUTH_TOKEN")
TWILIO_VERIFY_SERVICE_SID = env("TWILIO_VERIFY_SERVICE_SID")
TWILIO_SMS_CHANNEL = "sms"
