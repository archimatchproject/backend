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
    (GLOBAL_PATH, "footer_logo.png"),
)

ARCHITECT_REQUEST_IMAGES = (
    (GLOBAL_PATH, "architect_logo.png"),
    (GLOBAL_PATH, "architect_request_header.png"),
)
ARCHITECT_PASSWORD_IMAGES = (
    (GLOBAL_PATH, "architect_logo.png"),
    (GLOBAL_PATH, "architect_password_header.png"),
)
ACCEPT_ARCHITECT_REQUEST_IMAGES = (
    (GLOBAL_PATH, "architect_logo.png"),
    (GLOBAL_PATH, "accept_architect_request_header.png"),
)
REFUSE_ARCHITECT_REQUEST_IMAGES = (
    (GLOBAL_PATH, "architect_logo.png"),
    (GLOBAL_PATH, "refuse_architect_request_header.png"),
)

ADD_ADMIN_IMAGES = (
    (GLOBAL_PATH, "architect_logo.png"),
    (GLOBAL_PATH, "refuse_architect_request_header.png"),
)
CLIENT_PASSWORD_IMAGES = (
    (GLOBAL_PATH, "client_logo.png"),
    (GLOBAL_PATH, "client_password_header.png"),
)
