import re
from typing import Optional


def get_dollar_string(raw_str: str) -> Optional[str]:
    if m:=re.search(r"(?:\$(\d+(?:\.\d+)? \w+))", raw_str):
        return m.group(1)
    return None


def convert_str_to_number(number_str):
    pass
