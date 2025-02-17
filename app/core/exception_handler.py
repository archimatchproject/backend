"""_
This module provides custom exception handling for a Django REST framework application.
Classes:
    CustomAPIException: A custom API exception class that allows setting a custom status code.
Functions:
    extract_integrity_error_details(error_message):
    get_resource_name_from_exception(exception):
        Extracts the resource name from a DoesNotExist exception or its message.
    extract_validation_error_details(error):
        Extracts details from a ValidationError object, handling both string and dict error structures.
    handle_service_exceptions(func):
        A decorator that wraps a function to handle various service exceptions and raise a CustomAPIException.
"""

import logging
import re

from django.core.exceptions import ObjectDoesNotExist
from django.db import IntegrityError

from rest_framework import status
from rest_framework.exceptions import APIException
from rest_framework.exceptions import NotAuthenticated
from rest_framework.exceptions import NotFound
from rest_framework.exceptions import ParseError
from rest_framework.exceptions import PermissionDenied
from rest_framework.exceptions import Throttled
from rest_framework.exceptions import ValidationError


logger = logging.getLogger(__name__)


class CustomAPIException(APIException):
    """
    Custom exception class for API errors.
    Attributes:
        status_code (int): HTTP status code for the exception. Defaults to 500.
        default_detail (str): Default error message. Defaults to "A server error occurred."
        default_code (str): Default error code. Defaults to "error".
    Methods:
        __init__(self, detail=None, code=None, status_code=None):
            Initializes the CustomAPIException with optional detail, code, and status_code.
            Args:
                detail (str, optional): Custom error message. Defaults to None.
                code (str, optional): Custom error code. Defaults to None.
                status_code (int, optional): Custom HTTP status code. Defaults to None.
    """

    status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
    default_detail = "A server error occurred."
    default_code = "error"

    def __init__(self, detail=None, code=None, status_code=None):
        if detail is None:
            detail = self.default_detail
        if code is None:
            code = self.default_code

        super().__init__(detail=detail, code=code)
        if status_code is not None:
            self.status_code = status_code


EXCEPTION_MAPPINGS = {
    ValidationError: {
        "code": "validation_error",
        "message": "{error}",
        "status": status.HTTP_400_BAD_REQUEST,
    },
    PermissionDenied: {
        "code": "permission_denied",
        "message": "Permission Denied: {error}",
        "status": status.HTTP_403_FORBIDDEN,
    },
    NotAuthenticated: {
        "code": "not_authenticated",
        "message": "Authentication Required: {error}",
        "status": status.HTTP_401_UNAUTHORIZED,
    },
    NotFound: {
        "code": "not_found",
        "message": "Resource Not Found: {error}",
        "status": status.HTTP_404_NOT_FOUND,
    },
    ParseError: {
        "code": "parse_error",
        "message": "Parse Error: {error}",
        "status": status.HTTP_400_BAD_REQUEST,
    },
    Throttled: {
        "code": "throttled",
        "message": "Request Limit Exceeded: {error}",
        "status": status.HTTP_429_TOO_MANY_REQUESTS,
    },
    IntegrityError: {
        "code": "integrity_error",
        "message": "{error}",
        "status": status.HTTP_400_BAD_REQUEST,
    },
    APIException: {
        "code": "api_error",
        "message": "{error}",
        "status": status.HTTP_400_BAD_REQUEST,
    },
}


def extract_integrity_error_details(error_message):
    """
    Extracts and formats details from an IntegrityError message.
    """
    match = re.search(r"DETAIL:  Key \((\w+)\)=\(([^)]+)\) already exists\.", error_message)
    if match:
        field_name, field_value = match.groups()
        return f"Conflict with field '{field_name}' having value '{field_value}'"
    return error_message


def get_resource_name_from_exception(exception):
    """
    Extract the resource name from a DoesNotExist exception or its message.

    Args:
        exception (ObjectDoesNotExist): The exception instance.

    Returns:
        str: A human-readable resource name.
    """
    # Try to extract resource name from the exception message
    match = re.search(r"(\w+) matching query does not exist", str(exception))

    if match:
        # If the exception message contains the resource name, return it
        return match.group(1)

    # Fallback to extracting the resource name from the exception class name
    model_name = exception.__class__.__name__.replace("DoesNotExist", "")

    # Format the model name for better readability if needed (e.g., converting CamelCase to spaced
    # words)
    formatted_model_name = re.sub(r"(?<!^)(?=[A-Z])", " ", model_name)

    return formatted_model_name


def extract_validation_error_details(error):
    """
    Extracts details from a ValidationError object. This handles both string and dict error
    structures.
    """
    if isinstance(error.detail, dict):
        error_messages = []
        for field, messages in error.detail.items():
            if isinstance(messages, list):
                # Combine messages for a field
                for message in messages:
                    if isinstance(message, dict):
                        error_messages.append(f"{field}: {message.get('string', str(message))}")
                    else:
                        error_messages.append(f"{field}: {str(message)}")
            else:
                error_messages.append(f"{field}: {str(messages)}")
        return "; ".join(error_messages)
    elif isinstance(error.detail, list):
        return "; ".join([str(e) for e in error.detail])
    return str(error.detail)


def handle_service_exceptions(func):
    """
    A decorator that handles exceptions for service functions and raises custom API exceptions.
    Args:
        func (callable): The service function to be wrapped by the decorator.
    Returns:
        callable: The wrapped function with exception handling.
    Raises:
        CustomAPIException: If an exception occurs, a custom API exception is raised with appropriate details.
    Exception Handling:
        - Catches exceptions defined in EXCEPTION_MAPPINGS and raises a CustomAPIException with a formatted message.
        - Catches IntegrityError and extracts details using `extract_integrity_error_details`.
        - Catches ValidationError and extracts details using `extract_validation_error_details`.
        - Catches ObjectDoesNotExist and raises a CustomAPIException with a "not found" message.
        - Catches any other exceptions and raises a CustomAPIException with a generic internal error message.
    """

    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except tuple(EXCEPTION_MAPPINGS.keys()) as ex:
            exc_type = type(ex)
            error_info = EXCEPTION_MAPPINGS.get(
                exc_type,
                {
                    "code": "internal_error",
                    "message": "An internal error occurred.",
                    "status": status.HTTP_500_INTERNAL_SERVER_ERROR,
                },
            )

            if isinstance(ex, IntegrityError):
                # Extract details from IntegrityError
                detail = extract_integrity_error_details(str(ex))
            elif isinstance(ex, ValidationError):
                detail = extract_validation_error_details(ex)
            else:
                detail = str(ex)

            formatted_message = error_info["message"].format(
                error=detail
            )  # Format the message with the error detail
            logger.error(f"{formatted_message} - Details: {str(ex)}", exc_info=True)

            # Raise custom API exception with status_code
            raise CustomAPIException(
                detail=formatted_message,
                code=error_info["code"],
                status_code=error_info["status"],
            )
        except ObjectDoesNotExist as ex:
            resource_name = get_resource_name_from_exception(ex)
            detail = f"{resource_name} not found."
            logger.error(f"{detail} - Details: {str(ex)}", exc_info=True)
            raise CustomAPIException(
                detail=detail, code="not_found", status_code=status.HTTP_404_NOT_FOUND
            )
        except Exception as ex:
            logger.error("Unhandled Exception: %s", str(ex), exc_info=True)
            raise CustomAPIException(
                detail="An internal error occurred. Please contact support.",
                code="internal_error",
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

    return wrapper
