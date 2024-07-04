"""
Module for handling signals and background tasks
it receives the signal and call the background task
"""

from django.dispatch import receiver

from .signals import api_success_signal
from .tasks import send_email_background_task


@receiver(api_success_signal)
def run_background_task(sender, **kwargs):
    """
    Signal receiver function to initiate a background task upon receiving `api_success_signal`.

    Args:
        sender: The sender of the signal.
        **kwargs: Additional keyword arguments passed along with the signal.

    """
    data = kwargs.get("data")
    try:
        print("Signal received. Initiating background task...")
        send_email_background_task(data)

    except Exception as e:
        print(f"Task failed after retries with error: {e}")
