import pytest
from fbscraper.utils import get_dollar_string, convert_str_to_float


def test_get_dollar_string():
    assert get_dollar_string("$31 billion") == "31 billion"
    assert get_dollar_string("£10 million") is None
    assert get_dollar_string("$23.5 million") == "23.5 million"


def test_convert_string_to_float():
    assert convert_str_to_float("31 billion") == 31_000_000_000
    assert convert_str_to_float("31") == 31
