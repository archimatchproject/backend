"""
Module-level constants for env configuration.
"""

import pathlib

from django.core.exceptions import ImproperlyConfigured


BASE_DIR = pathlib.Path(__file__).resolve().parent.parent
APPS_DIR = BASE_DIR / "app"


def env_to_enum(enum_cls, value):
    """
    Method-level constants for env configuration.
    """
    for x in enum_cls:
        if x.value == value:
            return x
    raise ImproperlyConfigured(f"Env value {repr(value)} could not be found in {repr(enum_cls)}")
