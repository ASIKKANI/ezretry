import time
import functools
import logging
from typing import Tuple, Type, Union, Callable, Any

logger = logging.getLogger("ezretry")

def retry(
    exceptions: Union[Type[Exception], Tuple[Type[Exception], ...]] = Exception,
    tries: int = 3,
    delay: float = 1.0,
    backoff: float = 2.0,
    logger: Any = None
) -> Callable:
    """
    A decorator that retries a function with exponential backoff.

    :param exceptions: Exception class or tuple of exception classes to catch. Defaults to Exception.
    :param tries: Max number of attempts. Must be >= 1. Defaults to 3.
    :param delay: Initial delay between retries in seconds. Must be >= 0. Defaults to 1.0.
    :param backoff: Multiplier to apply to the delay after each retry. Must be >= 1.0.
    :param logger: Optional logger instance. If provided, retries will be logged.
    """
    if tries < 1:
        raise ValueError("tries must be 1 or greater")
    if delay < 0:
        raise ValueError("delay must be 0 or greater")
    if backoff < 1.0:
        raise ValueError("backoff multiplier must be 1.0 or greater")

    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            attempt_tries = tries
            current_delay = delay
            
            while attempt_tries > 0:
                try:
                    return func(*args, **kwargs)
                except exceptions as e:
                    attempt_tries -= 1
                    if attempt_tries == 0:
                        raise e
                    
                    if logger:
                        logger.warning(
                            f"Function '{func.__name__}' raised {e.__class__.__name__}: {e}. "
                            f"Retrying in {current_delay:.2f} seconds (attempts remaining: {attempt_tries})..."
                        )
                    
                    time.sleep(current_delay)
                    current_delay *= backoff

        return wrapper
    return decorator
