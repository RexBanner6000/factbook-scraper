import pytest
from fbscraper.utils import get_dollar_string


def test_get_dollar_string():
    assert get_dollar_string("$31 billion") == "31 billion"
    assert get_dollar_string("£10 million") is None
    assert get_dollar_string("$23.5 million") == "23.5 million"
