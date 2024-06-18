from project_core.django.base import *

DEBUG = True


ALLOWED_HOSTS = ["archimatch-backend.azurewebsites.net",]
CSRF_TRUSTED_ORIGINS = ["https://archimatch-backend.azurewebsites.net",]
STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"