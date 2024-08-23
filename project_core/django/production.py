"""
Module-level constants for production configuration.
"""

from project_core.django.base import *
from project_core.env import env


DEBUG = env("DEBUG")



AZURE_ACCOUNT_NAME=env("AZURE_ACCOUNT_NAME")
AZURE_ACCOUNT_KEY=env("AZURE_ACCOUNT_KEY")
AZURE_CONTAINER=env("AZURE_CONTAINER")
DEFAULT_FILE_STORAGE = "storages.backends.azure_storage.AzureStorage"
STATICFILES_STORAGE = "storages.backends.azure_storage.AzureStorage"

"""
Static files (CSS, JavaScript, Images) serving configuration.
"""
STATIC_URL = f"https://{AZURE_ACCOUNT_NAME}.blob.core.windows.net/{AZURE_CONTAINER}/static/"
STATIC_ROOT = ""
STATICFILES_STORAGE = "storages.backends.azure_storage.AzureStorage"

"""
Media files (uploads) configuration.
"""
MEDIA_URL = f"https://{AZURE_ACCOUNT_NAME}.blob.core.windows.net/{AZURE_CONTAINER}/media/"
MEDIA_ROOT = ""
DEFAULT_FILE_STORAGE = "storages.backends.azure_storage.AzureStorage"