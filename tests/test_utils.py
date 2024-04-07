import pytest

from fbscraper.utils import (
    convert_str_to_float,
    get_country_name,
    get_death_rate_from_string,
    get_distance_from_str,
    get_dollar_string,
    get_electricity_from_str,
    get_percentage_from_string,
)


def test_get_dollar_string():
    assert get_dollar_string("$31 billion") == 31_000_000_000
    assert get_dollar_string("£10 million") is None
    assert get_dollar_string("$23.5 million") == 23_500_000
    assert get_dollar_string("$1,234,567") == 1_234_567


def test_convert_string_to_float():
    assert convert_str_to_float("31 billion") == 31_000_000_000
    assert convert_str_to_float("31") == 31


def test_get_percentage_string():
    assert get_percentage_from_string("50%") == 0.5
    assert get_percentage_from_string("10004.43%") == 100.0443
    assert get_percentage_from_string("75") is None


def test_get_country_name():
    assert get_country_name("     Afghanistan") == "Afghanistan"


def test_get_distance_from_string():
    assert get_distance_from_str("10 km") == 10
    assert get_distance_from_str("1,000.5 km") == 1000.5
    assert get_distance_from_str("100km") == 100
    assert get_distance_from_str("100") is None
    assert get_distance_from_str("0 km") == 0


def test_get_death_rate_from_string():
    assert get_death_rate_from_string("12.7 deaths per 1000") == 12.7
    assert get_death_rate_from_string("10 deaths per 1000") == 10
    assert get_death_rate_from_string("10 per 1000") is None


def test_get_electricity_from_str():
    assert (
        get_electricity_from_str("Afghanistan	453.75 million kWh (2000)")
        == 453_750_000
    )
    assert get_electricity_from_str("5,205.4 kWh") == 5205.4
