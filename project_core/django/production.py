"""
Module-level constants for production configuration.
"""

from project_core.django.base import *


DEBUG = True


ALLOWED_HOSTS = [
    "archimatch-backend.azurewebsites.net",
    "archimatch-backend-test.azurewebsites.net"
]
CSRF_TRUSTED_ORIGINS = [
    "https://archimatch-backend.azurewebsites.net",
    "https://archimatch-backend-test.azurewebsites.net"
]
