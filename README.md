# ezretry-asik

A lightweight, beginner-friendly Python decorator to automatically retry failing operations with configurable exponential backoff and exception filtering.

---

## Features

- **Simple Decorator Syntax:** Wrap any function with `@retry` to instantly add resilience.
- **Exponential Backoff:** Configurable delay multiplier to progressively wait longer between retries, giving downstream systems time to recover.
- **Targeted Exception Filtering:** Specify exactly which errors should trigger a retry, allowing developer bugs (like `KeyError` or `NameError`) to fail fast.
- **Signature Preservation:** Retains the original function's docstring, name, and parameter signature using `functools.wraps`.
- **Zero External Dependencies:** Pure Python implementation utilizing only standard library modules (`time` and `functools`).

---

## Installation

Install the library directly from PyPI: 

```bash
pip install ezretry-asik
```

Or install locally for development:

```bash
pip install -e .
```

---

## Usage Guide

### Basic Usage
By default, the decorator retries any raised exception up to 3 times, with a constant 1-second delay between attempts.

```python
from ezretry import retry

@retry(tries=3)
def fetch_api_data():
    # This call will run up to 3 times if any exception occurs.
    # It waits 1.0 second between attempts.
    return request_network_resource()
```

### Specifying Target Exceptions
To prevent retrying on syntax errors, division by zero, or logical bugs, restrict retries to specific exceptions (such as network or connection timeouts).

```python
from ezretry import retry

@retry(exceptions=(ConnectionError, TimeoutError), tries=4)
def upload_payload():
    # Only ConnectionError or TimeoutError will trigger a retry.
    # A TypeError or ValueError will crash immediately.
    return send_data()
```

### Understanding Exponential Backoff
The backoff multiplier determines how the sleep interval increases after each consecutive failure.

The delay for attempt `N` is calculated as:
`current_delay = delay * (backoff ^ (N - 1))`

Here is an example setup with 5 attempts, a base delay of 1.5 seconds, and a backoff multiplier of 2.0:

```python
from ezretry import retry

@retry(tries=5, delay=1.5, backoff=2.0)
def process_transaction():
    raise ConnectionError("Server connection failed")
```

If the function fails continuously, the wait times between attempts behave as follows:

| Attempt | Status | Delay Before Next Attempt | Cumulative Time Waited |
| :--- | :--- | :--- | :--- |
| 1 | Failed | 1.5 seconds | 1.5 seconds |
| 2 | Failed | 3.0 seconds | 4.5 seconds |
| 3 | Failed | 6.0 seconds | 10.5 seconds |
| 4 | Failed | 12.0 seconds | 22.5 seconds |
| 5 | Failed | Raises final exception | 22.5 seconds |

### Integrating a Custom Logger
Pass a standard Python logger instance to log warnings automatically before each retry sleep.

```python
import logging
from ezretry import retry

logging.basicConfig(level=logging.WARNING)
app_logger = logging.getLogger("network")

@retry(tries=3, delay=1.0, logger=app_logger)
def database_query():
    raise RuntimeError("Query timed out")
```

This configuration prints the following warning messages to the console:
```text
WARNING:network:Function 'database_query' raised RuntimeError: Query timed out. Retrying in 1.00 seconds (attempts remaining: 2)...
WARNING:network:Function 'database_query' raised RuntimeError: Query timed out. Retrying in 2.00 seconds (attempts remaining: 1)...
```

---

## Configuration Reference

| Parameter | Type | Default | Description |
| :--- | :--- | :--- | :--- |
| `exceptions` | `Exception` or `tuple[Exception, ...]` | `Exception` | The exception types to catch and retry. |
| `tries` | `int` | `3` | Maximum number of attempts (must be greater than or equal to 1). |
| `delay` | `float` | `1.0` | Initial delay between retries in seconds (must be greater than or equal to 0). |
| `backoff` | `float` | `2.0` | Multiplier applied to the delay after each failure (must be greater than or equal to 1.0). |
| `logger` | `logging.Logger` | `None` | Optional logger to print warning messages. |

---

## License

This project is licensed under the MIT License.
