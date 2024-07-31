"""
Module-level constants for backend and frontend URLs, and CORS configuration.
"""

import os

import environ


env = environ.Env()
env.read_env(os.path.join(os.path.dirname(__file__), ".env"))

BASE_BACKEND_URL = ""
BASE_FRONTEND_URL = (
    f"http://{env('DNS_ADDRESS')}:3000" if env("IS_LOCAL") else f"https://{env('DNS_ADDRESS')}"
)

# CORS_ALLOWED_ORIGINS = [BASE_FRONTEND_URL]
CORS_ALLOW_ALL_ORIGINS = True
