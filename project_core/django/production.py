"""
Module-level constants for production configuration.
"""

from project_core.django.base import *
from project_core.env import env


DEBUG = env("DEBUG")

CORS_ALLOW_ALL_ORIGINS = False
