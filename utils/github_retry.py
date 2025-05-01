# utils/github_retry.py

import time
import functools
import logging
from typing import Callable

logger = logging.getLogger(__name__)


def with_retries(max_attempts: int = 3, delay_seconds: float = 1.0, backoff_factor: float = 2.0):
    """
    Retry decorator for handling transient GitHub API errors.
    Usage:
        @with_retries()
        def call(): ...
    """
    def decorator(func: Callable):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            attempts = 0
            delay = delay_seconds
            while attempts < max_attempts:
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    attempts += 1
                    if attempts == max_attempts:
                        logger.error(f"GitHub call failed after {attempts} attempts: {e}")
                        raise
                    logger.warning(f"Retrying GitHub call ({attempts}/{max_attempts}) due to: {e}")
                    time.sleep(delay)
                    delay *= backoff_factor
        return wrapper
    return decorator
