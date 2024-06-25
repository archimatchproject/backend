"""
Module-level constants for translation configuration.
"""
from project_core.env import BASE_DIR

LANGUAGES = [
    ("en", "English"),
    ("fr", "French"),
    ("ar", "Arabic"),
]

LANGUAGE_CODE = "en"

LOCALE_PATHS = [
    BASE_DIR / "locale",
]
TIME_ZONE = "UTC"
USE_I18N = True
USE_L10N = True
USE_TZ = True

MODELTRANSLATION_DEFAULT_LANGUAGE = "en"
MODELTRANSLATION_LANGUAGES = ("en", "fr", "ar")
