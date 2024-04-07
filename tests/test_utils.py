import pytest

from fbscraper import utils


def test_get_dollar_string():
    assert utils.get_dollar_string("$31 billion") == 31_000_000_000
    assert utils.get_dollar_string("£10 million") is None
    assert utils.get_dollar_string("$23.5 million") == 23_500_000
    assert utils.get_dollar_string("$1,234,567") == 1_234_567


def test_convert_string_to_float():
    assert utils.convert_str_to_float("31 billion") == 31_000_000_000
    assert utils.convert_str_to_float("31") == 31


def test_get_percentage_string():
    assert utils.get_percentage_from_string("50%") == 0.5
    assert utils.get_percentage_from_string("10004.43%") == 100.0443
    assert utils.get_percentage_from_string("75") is None


def test_get_country_name():
    assert utils.get_country_name("     Afghanistan") == "Afghanistan"


def test_get_distance_from_string():
    assert utils.get_distance_from_str("10 km") == 10
    assert utils.get_distance_from_str("1,000.5 km") == 1000.5
    assert utils.get_distance_from_str("100km") == 100
    assert utils.get_distance_from_str("100") is None
    assert utils.get_distance_from_str("0 km") == 0


def test_get_death_rate_from_string():
    assert utils.get_death_rate_from_string("12.7 deaths per 1000") == 12.7 / 1000
    assert utils.get_death_rate_from_string("10 deaths per 1000") == 10 / 1000
    assert utils.get_death_rate_from_string("10 per 1000") is None
