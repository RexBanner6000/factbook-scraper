import pytest
from fbscraper.utils import get_dollar_string, convert_str_to_float, get_percentage_from_string


def test_get_dollar_string():
    assert get_dollar_string("$31 billion") == "31 billion"
    assert get_dollar_string("£10 million") is None
    assert get_dollar_string("$23.5 million") == "23.5 million"


def test_convert_string_to_float():
    assert convert_str_to_float("31 billion") == 31_000_000_000
    assert convert_str_to_float("31") == 31


def test_get_percentage_string():
    assert get_percentage_from_string("50%") == 0.5
    assert get_percentage_from_string("10004.43%") == 100.0443
    assert get_percentage_from_string("75") is None
