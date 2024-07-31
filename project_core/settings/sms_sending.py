"""
Module-level constants for Twilio configuration.
"""

import os

import environ

from project_core.env import BASE_DIR


env = environ.Env()
environ.Env.read_env(os.path.join(BASE_DIR, ".env"))

TWILIO_ACCOUNT_SID = env("TWILIO_ACCOUNT_SID")
TWILIO_AUTH_TOKEN = env("TWILIO_AUTH_TOKEN")
TWILIO_VERIFY_SERVICE_SID = env("TWILIO_VERIFY_SERVICE_SID")
TWILIO_SMS_CHANNEL = "sms"
