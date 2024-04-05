import re
from typing import Optional


def get_dollar_string(raw_str: str) -> Optional[str]:
    if m := re.search(r"(?:\$(\d+(?:\.\d+)? \w+))", raw_str):
        return m.group(1)
    return None


def convert_str_to_float(number_str: str) -> float:
    multipliers = {
        "thousand": 1000,
        "million": 1_000_000,
        "billion": 1_000_000_000,
        "trillion": 1_000_000_000_000,
    }
    string_split = number_str.split(" ")
    if len(string_split) == 1:
        return float(number_str)
    return float(string_split[0]) * multipliers[string_split[1]]


def get_percentage_from_string(raw_str: str) -> Optional[float]:
    if m := re.search(r"(\d+(?:\.\d+)?)%", raw_str):
        return float(m.group(1)) / 100
    return None


def get_country_name(raw_str: str) -> Optional[str]:
    if m := re.search(r"\w[\w ]+", raw_str):
        return m.group(0)
    return None


def get_field_types(fb_type: str = "local"):
    if fb_type == "local":
        parent_type = "tr"
        child_type = "td"
    elif fb_type == "web":
        parent_type = "div"
        child_type = "h3"
    else:
        parent_type = None
        child_type = None
    return parent_type, child_type


def get_age_structures(raw_str: str) -> Optional[dict[str, float]]:
    pattern = re.compile(
        r"(?:(\d{1,2}(?:-\d{1,2})?) years:?(?: and over:)?\s?(\d{1,2}(?:\.\d{1,2})?)%)"
    )
    if m := re.findall(pattern, raw_str):
        age_structure = {x[0]: float(x[1])/100 for x in m}
        return age_structure
    return None
