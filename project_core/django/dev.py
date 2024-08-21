"""
Module-level constants for dev configuration.
"""

from project_core.django.base import *
from project_core.env import env
import os

DEBUG = env("DEBUG")
"""
Static files (CSS, JavaScript, Images) serving configuration.
"""
STATIC_URL = "/static/"
STATIC_ROOT = os.path.join(BASE_DIR, "static/")
"""
Media files (uploads) configuration.
"""
MEDIA_ROOT = os.path.join(BASE_DIR, "media")
MEDIA_URL = "/media/"