"""
Module-level constants for email_sending configuration.
"""

# Email configuration

EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
EMAIL_HOST = "smtp.gmail.com"
EMAIL_PORT = 587
EMAIL_USE_TLS = True
DEFAULT_FROM_EMAIL = "ArchiMatch"
EMAIL_HOST_USER = "ghazichaftar@gmail.com"
EMAIL_HOST_PASSWORD = "rfbq luxr lzmk pxom"


MAX_ATTEMPTS = 5
BACKGROUND_TASK_RUN_ASYNC = True
TOKEN_VALIDITY = 600
TOKEN_SALT = "B+I-/I.]po68Y=HmubAHZYqufX.f.\S*\:2T),*yI,v87MKa#Es}-iy'UdiY=Ljt"  # noqa
