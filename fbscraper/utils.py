import re
from typing import Optional


def get_dollar_string(raw_str: str) -> Optional[str]:
    if m:=re.search(r"(?:\$(\d+(?:\.\d+)? \w+))", raw_str):
        return m.group(1)
    return None


def convert_str_to_float(number_str: str) -> float:
    multipliers = {
        "thousand": 1000,
        "million": 1_000_000,
        "billion": 1_000_000_000,
        "trillion": 1_000_000_000_000
    }
    string_split = number_str.split(" ")
    if len(string_split) == 1:
        return float(number_str)
    return float(string_split[0]) * multipliers[string_split[1]]


def get_percentage_from_string(raw_str: str) -> Optional[float]:
    if m := re.search(r"(\d+(?:\.\d+)?)%", raw_str):
        return float(m.group(1)) / 100
    return None
