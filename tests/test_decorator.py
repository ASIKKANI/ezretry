import pytest
import time
from unittest.mock import patch, MagicMock
from ezretry import retry

def test_success_on_first_try():
    call_count = 0

    @retry(tries=3)
    def my_func():
        nonlocal call_count
        call_count += 1
        return "success"

    result = my_func()
    assert result == "success"
    assert call_count == 1

@patch("time.sleep")
def test_retry_eventual_success(mock_sleep):
    call_count = 0

    @retry(tries=3, delay=1.0, backoff=2.0)
    def my_func():
        nonlocal call_count
        call_count += 1
        if call_count < 3:
            raise ValueError("failing")
        return "success"

    result = my_func()
    assert result == "success"
    assert call_count == 3
    # Check time.sleep was called with exponential delay
    assert mock_sleep.call_count == 2
    mock_sleep.assert_any_call(1.0)
    mock_sleep.assert_any_call(2.0)

@patch("time.sleep")
def test_retry_exhausted(mock_sleep):
    call_count = 0

    @retry(tries=3, delay=1.0, backoff=2.0)
    def my_func():
        nonlocal call_count
        call_count += 1
        raise ValueError("failing forever")

    with pytest.raises(ValueError, match="failing forever"):
        my_func()

    assert call_count == 3
    assert mock_sleep.call_count == 2
    mock_sleep.assert_any_call(1.0)
    mock_sleep.assert_any_call(2.0)

@patch("time.sleep")
def test_different_exception_not_caught(mock_sleep):
    call_count = 0

    @retry(exceptions=ValueError, tries=3)
    def my_func():
        nonlocal call_count
        call_count += 1
        raise KeyError("unexpected error")

    # Should raise KeyError immediately (no retries)
    with pytest.raises(KeyError, match="unexpected error"):
        my_func()

    assert call_count == 1
    assert mock_sleep.call_count == 0

def test_invalid_parameters():
    with pytest.raises(ValueError, match="tries must be 1 or greater"):
        retry(tries=0)

    with pytest.raises(ValueError, match="delay must be 0 or greater"):
        retry(delay=-1.0)

    with pytest.raises(ValueError, match="backoff multiplier must be 1.0 or greater"):
        retry(backoff=0.5)
