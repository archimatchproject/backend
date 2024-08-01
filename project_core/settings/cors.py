"""
Module-level constants for backend and frontend URLs, and CORS configuration.
"""

from project_core.env import env


DNS_ADDRESS = env("DNS_ADDRESS")

BASE_FRONTEND_URL = f"http://{DNS_ADDRESS}:3000" if env("IS_LOCAL") else f"http://{DNS_ADDRESS}"

# CORS_ALLOWED_ORIGINS = [BASE_FRONTEND_URL]

ALLOWED_HOSTS = ["localhost", "127.0.0.1"] if env("IS_LOCAL") else [f"{DNS_ADDRESS}"]
CSRF_TRUSTED_ORIGINS = [] if env("IS_LOCAL") else [f"http://{DNS_ADDRESS}"]
