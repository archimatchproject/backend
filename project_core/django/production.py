"""
Module-level constants for production configuration.
"""

from project_core.django.base import *
from project_core.env import env


DEBUG = env("DEBUG")
