"""
Module-level constants for images sent in emails.
"""

from project_core.env import BASE_DIR


ICONS_PATH = r"/media/icons"
GLOBAL_PATH = str(BASE_DIR) + ICONS_PATH


def generate_image_paths(*images):
    """
    generates the list of images for sending emails
    """
    return [(GLOBAL_PATH, img) if isinstance(img, str) else img for img in images]


COMMON_IMAGES = generate_image_paths(
    "facebook.png", "instagram.png", "twitter.png", "footer_logo.png"
)

ARCHITECT_REQUEST_IMAGES = generate_image_paths(
    *COMMON_IMAGES, "architect_logo.png", "architect_request_header.png"
)

ARCHITECT_PASSWORD_IMAGES = generate_image_paths(
    *COMMON_IMAGES, "architect_logo.png", "architect_password_header.png"
)

ACCEPT_ARCHITECT_REQUEST_IMAGES = generate_image_paths(
    *COMMON_IMAGES, "architect_logo.png", "accept_architect_request_header.png"
)

REFUSE_ARCHITECT_REQUEST_IMAGES = generate_image_paths(
    *COMMON_IMAGES, "architect_logo.png", "refuse_architect_request_header.png"
)

ADD_ADMIN_IMAGES = generate_image_paths(
    *COMMON_IMAGES, "architect_logo.png", "refuse_architect_request_header.png"
)

CLIENT_PASSWORD_IMAGES = generate_image_paths(
    *COMMON_IMAGES, "client_logo.png", "client_password_header.png"
)
