from django.db import IntegrityError
from rest_framework.exceptions import (
    APIException,
    ValidationError,
    PermissionDenied,
    NotAuthenticated,
    NotFound,
    ParseError,
    Throttled
)
import logging
from rest_framework import status
import re
# Set up a logger
logger = logging.getLogger(__name__)



class CustomAPIException(APIException):
    status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
    default_detail = 'A server error occurred.'
    default_code = 'error'

    def __init__(self, detail=None, code=None, status_code=None):
        if detail is None:
            detail = self.default_detail
        if code is None:
            code = self.default_code

        super().__init__(detail=detail, code=code)
        if status_code is not None:
            self.status_code = status_code

# Exception mappings including IntegrityError and APIException, with status codes
EXCEPTION_MAPPINGS = {
    ValidationError: {"code": "validation_error", "message": "Validation Error: {error}", "status": status.HTTP_400_BAD_REQUEST},
    PermissionDenied: {"code": "permission_denied", "message": "Permission Denied: {error}", "status": status.HTTP_403_FORBIDDEN},
    NotAuthenticated: {"code": "not_authenticated", "message": "Authentication Required: {error}", "status": status.HTTP_401_UNAUTHORIZED},
    NotFound: {"code": "not_found", "message": "Resource Not Found: {error}", "status": status.HTTP_404_NOT_FOUND},
    ParseError: {"code": "parse_error", "message": "Parse Error: {error}", "status": status.HTTP_400_BAD_REQUEST},
    Throttled: {"code": "throttled", "message": "Request Limit Exceeded: {error}", "status": status.HTTP_429_TOO_MANY_REQUESTS},
    IntegrityError: {"code": "integrity_error", "message": "{error}", "status": status.HTTP_400_BAD_REQUEST},
    APIException: {"code": "api_error", "message": "{error}", "status": status.HTTP_400_BAD_REQUEST}
}

def extract_integrity_error_details(error_message):
    """
    Extracts and formats details from an IntegrityError message.
    """
    # Example: psycopg2.errors.UniqueViolation: duplicate key value violates unique constraint "users_archimatchuser_username_key"
    # DETAIL:  Key (username)=(ghazichaftar@gmail.com) already exists.
    match = re.search(r'DETAIL:  Key \((\w+)\)=\(([^)]+)\) already exists\.', error_message)
    if match:
        field_name, field_value = match.groups()
        return f"Conflict with field '{field_name}' having value '{field_value}'"
    return error_message

def handle_service_exceptions(func):
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except tuple(EXCEPTION_MAPPINGS.keys()) as ex:
            exc_type = type(ex)
            error_info = EXCEPTION_MAPPINGS.get(exc_type, {"code": "internal_error", "message": "An internal error occurred.", "status": status.HTTP_500_INTERNAL_SERVER_ERROR})

            if isinstance(ex, IntegrityError):
                # Extract details from IntegrityError
                detail = extract_integrity_error_details(str(ex))
            else:
                detail = str(ex)
            
            formatted_message = error_info['message'].format(error=detail)  # Format the message with the error detail
            logger.error(f"{formatted_message} - Details: {str(ex)}", exc_info=True)
            
            # Raise custom API exception with status_code
            raise CustomAPIException(detail=formatted_message, code=error_info['code'], status_code=error_info['status'])
        except Exception as ex:
            # Log the full error details for internal debugging
            logger.error("Unhandled Exception: %s", str(ex), exc_info=True)
            
            # Return a generic error message to the client with a 500 status
            raise CustomAPIException(detail="An internal error occurred. Please contact support.", code="internal_error", status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
    return wrapper