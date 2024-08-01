"""
Module-level constants for dev configuration.
"""

from project_core.django.base import *
from project_core.env import env


DEBUG = env("DEBUG")

CORS_ALLOW_ALL_ORIGINS = True
