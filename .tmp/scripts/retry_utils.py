#!/usr/bin/env python3
"""
Shared retry utilities for all agent skills.

Provides:
- retry_with_backoff: Retry a function with exponential backoff
- safe_api_call: Wrap API calls with retry logic
- RateLimiter: Token-bucket rate limiter
"""
import time
import random
from functools import wraps
from typing import Callable, TypeVar

T = TypeVar("T")


def retry_with_backoff(
    func: Callable[..., T],
    max_retries: int = 3,
    base_delay: float = 1.0,
    max_delay: float = 60.0,
    backoff_factor: float = 2.0,
    exceptions: tuple = (Exception,),
) -> Callable[..., T]:
    """Decorator/factory to retry a function with exponential backoff."""
    @wraps(func)
    def wrapper(*args, **kwargs):
        delay = base_delay
        last_exception = None
        for attempt in range(max_retries + 1):
            try:
                return func(*args, **kwargs)
            except exceptions as e:
                last_exception = e
                if attempt < max_retries:
                    jitter = delay * random.uniform(0.5, 1.5)
                    time.sleep(min(jitter, max_delay))
                    delay *= backoff_factor
        raise last_exception  # type: ignore[misc]
    return wrapper


class RateLimiter:
    """Simple token-bucket rate limiter for API calls."""

    def __init__(self, calls_per_second: float = 1.0):
        self.rate = calls_per_second
        self.interval = 1.0 / calls_per_second if calls_per_second > 0 else 0
        self._last_call = 0.0

    def wait(self) -> None:
        """Wait until the next call is allowed."""
        now = time.monotonic()
        elapsed = now - self._last_call
        if elapsed < self.interval:
            time.sleep(self.interval - elapsed)
        self._last_call = time.monotonic()

    def __call__(self, func: Callable) -> Callable:
        """Use as decorator."""
        @wraps(func)
        def wrapper(*args, **kwargs):
            self.wait()
            return func(*args, **kwargs)
        return wrapper


def safe_api_call(
    func: Callable[..., T],
    *args,
    max_retries: int = 3,
    rate_limit: float = 0,
    **kwargs,
) -> T:
    """Call an API function with retry and optional rate limiting.

    Args:
        func: The function to call
        *args: Positional arguments for func
        max_retries: Maximum retry attempts
        rate_limit: Calls per second (0 = no limit)
        **kwargs: Keyword arguments for func

    Returns:
        The return value of func
    """
    limiter = RateLimiter(rate_limit) if rate_limit > 0 else None

    for attempt in range(max_retries + 1):
        try:
            if limiter:
                limiter.wait()
            return func(*args, **kwargs)
        except Exception as e:
            if attempt >= max_retries:
                raise
            delay = (2 ** attempt) * random.uniform(0.5, 1.5)
            time.sleep(min(delay, 30.0))
    # Unreachable — last iteration raises
    raise RuntimeError("safe_api_call: unreachable")


__all__ = ["retry_with_backoff", "RateLimiter", "safe_api_call"]
