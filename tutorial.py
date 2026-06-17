"""
ezretry Tutorial and Demonstration

This script teaches you how to use the 'ezretry' package. Run this file in your 
terminal to see how the decorator behaves in real-time.
"""

import time
import logging
from ezretry import retry

# Configure logging to print warnings when a retry occurs.
# In a real application, you would configure this in your main entry point.
logging.basicConfig(level=logging.WARNING, format="%(levelname)s: %(message)s")
logger = logging.getLogger("tutorial")


# =====================================================================
# Example 1: Basic Retry (Constant Delay)
# =====================================================================
print("======================================================================")
print("1. RUNNING BASIC RETRY EXAMPLE (Constant Delay)")
print("======================================================================")

# This decorator instructs Python to retry the function up to 3 times
# if ANY exception occurs, waiting 1.0 second between each attempt.
@retry(tries=3, delay=1.0)
def unstable_ping():
    print("Attempting connection to unstable server...")
    raise ConnectionError("Server did not respond.")

try:
    start_time = time.time()
    unstable_ping()
except ConnectionError as e:
    elapsed = time.time() - start_time
    print(f"\nFinal outcome: The function failed all attempts.")
    print(f"Error caught: {e}")
    print(f"Total time elapsed: {elapsed:.2f} seconds.")
    print("Explanation: Attempt 1 ran, failed, and slept 1s. Attempt 2 ran, failed, and slept 1s. Attempt 3 ran, failed, and raised the error.\n")


# =====================================================================
# Example 2: Exponential Backoff (Wait longer after each failure)
# =====================================================================
print("======================================================================")
print("2. RUNNING EXPONENTIAL BACKOFF EXAMPLE")
print("======================================================================")

attempts_counter = 0

# delay=0.5: First wait time is 0.5 seconds.
# backoff=2.0: Double the wait time after each consecutive failure.
# logger=logger: Automatically log a warning to stdout before sleeping.
@retry(tries=3, delay=0.5, backoff=2.0, logger=logger)
def fetch_api_data():
    global attempts_counter
    attempts_counter += 1
    
    print(f"Attempt #{attempts_counter} to fetch API payload...")
    if attempts_counter < 3:
        raise ValueError("Timeout reading data package.")
    return "API Success!"

start_time = time.time()
result = fetch_api_data()
elapsed = time.time() - start_time

print(f"\nFinal outcome: {result}")
print(f"Total attempts made: {attempts_counter}")
print(f"Total time elapsed: {elapsed:.2f} seconds.")
print("Explanation: First attempt failed -> slept 0.5s. Second attempt failed -> slept 1.0s (0.5 * 2.0). Third attempt succeeded.\n")


# =====================================================================
# Example 3: Exception Filtering (Fail fast on bugs)
# =====================================================================
print("======================================================================")
print("3. RUNNING EXCEPTION FILTERING EXAMPLE")
print("======================================================================")

# exceptions=ValueError: Only retry if a ValueError occurs.
# If a different exception occurs, crash immediately (do not wait or retry).
@retry(exceptions=ValueError, tries=3, delay=0.5)
def parse_database_record():
    print("Attempting to parse database entry...")
    # Raising a ZeroDivisionError, which is NOT a ValueError
    return 100 / 0

try:
    parse_database_record()
except ZeroDivisionError:
    print("\nOutcome: Correctly caught ZeroDivisionError instantly.")
    print("Explanation: The decorator filtered out this exception, bypassing retries. This is crucial so that bugs in your code fail fast rather than stalling execution.\n")


# =====================================================================
# Example 4: Metadata Preservation (Clean API design)
# =====================================================================
print("======================================================================")
print("4. RUNNING METADATA PRESERVATION CHECK")
print("======================================================================")

@retry(tries=2)
def calculate_metrics(x, y):
    """Computes telemetry values based on input parameters."""
    return x + y

# A common issue with custom decorators is that they wipe out the original
# function's name and docstring. ezretry uses functools.wraps to prevent this.
print(f"Function Name: '{calculate_metrics.__name__}'")
print(f"Docstring:     '{calculate_metrics.__doc__}'")
print("Explanation: Your code can safely inspect signatures, run auto-documentation tools, and print accurate tracebacks.\n")

print("======================================================================")
print("TUTORIAL COMPLETE")
print("======================================================================")
