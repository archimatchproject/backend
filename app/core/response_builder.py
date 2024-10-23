"""
Module: app.core.response_builder

Provides utility functions for creating standardized API responses with Django REST Framework.
Includes:
- `build_response`: Constructs a consistent API response format with success status, message, and data.
"""
from rest_framework.response import Response

def build_response(success=True, message='', data=None, status=200):
    """
    Build a standardized API response.

    Args:
        success (bool): Indicates if the request was successful.
        message (str): A message related to the response.
        data (dict or list): The data to be included in the response.
        status (int): HTTP status code.

    Returns:
        Response: A DRF Response object with the standardized format.
    """
    response_data = {
        'success': success,
        'message': message,
        'data': data if data is not None else {}
    }
    return Response(response_data, status=status)
