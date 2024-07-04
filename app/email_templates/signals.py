"""
Signal: api_success_signal

This signal is triggered when an API interaction is successful.
Listeners can connect to this signal to perform additional actions
when such events occur in the Django application.
"""

from django.dispatch import Signal


api_success_signal = Signal()
