"""
Module-level constants for images sent in emails.
"""

from project_core.env import BASE_DIR


ICONS_PATH = r"/media/icons"
GLOBAL_PATH = str(BASE_DIR) + ICONS_PATH
COMMON_IMAGES = (
    (GLOBAL_PATH, "facebook.png"),
    (GLOBAL_PATH, "instagram.png"),
    (GLOBAL_PATH, "twitter.png"),
    (GLOBAL_PATH, "architect_logo.png"),
    (GLOBAL_PATH, "welcome_architect_header.png"),
)
