"""
Module-level constants for backend and frontend URLs, and CORS configuration.
"""

import environ


env = environ.Env()
environ.Env.read_env()

BASE_BACKEND_URL = ""
BASE_FRONTEND_URL = (
    f"http://{env('DNS_ADDRESS')}:3000" if env("IS_LOCAL") else f"https://{env('DNS_ADDRESS')}"
)

# CORS_ALLOWED_ORIGINS = [BASE_FRONTEND_URL]
CORS_ALLOW_ALL_ORIGINS = True
