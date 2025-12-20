"""Tests for sanitize_text helper."""

import pytest

from slack_impl.slack_client import sanitize_text


@pytest.mark.unit
class TestSanitizeText:
    """Validate text normalization behavior."""

    def test_non_string_input_is_converted(self) -> None:
        """Non-string input is coerced to string."""
        result = sanitize_text(123)

        assert result == "123"

    def test_excess_whitespace_is_collapsed(self) -> None:
        """Multiple spaces collapse to one."""
        result = sanitize_text("hello    world")

        assert result == "hello world"

    def test_text_is_truncated(self) -> None:
        """Text longer than max_len is truncated."""
        result = sanitize_text("a" * 2000, max_len=10)

        assert len(result) == 10
