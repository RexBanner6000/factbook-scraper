import re
from typing import List, Optional
from bs4 import BeautifulSoup


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
    if m := re.search(r"(-?\d+(?:\.\d+)?)%", raw_str):
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
        age_structure = {x[0]: float(x[1]) / 100 for x in m}
        return age_structure
    return None


def get_areas_from_str(raw_str: str) -> Optional[dict[str, float]]:
    if m := re.findall(
        r"(\w+):[ \n]?((?:\d{1,3},?)+(?:\.\d+)?)\s(\w+\s)?sq km(?: less than)?",
        raw_str,
    ):
        areas = {}
        for match in m:
            if match[-1] == "":
                areas[match[0] + "_area"] = float(match[1].replace(",", ""))
            else:
                areas[match[0] + "_area"] = convert_str_to_float(
                    f"{match[1]} {match[2]}"
                )
        return areas
    return None


def get_distance_from_str(raw_str: str) -> Optional[float]:
    if m := re.search(r"((?:\d{1,3},?)+(?:\.\d+)?)+\s?km", raw_str):
        return float(m.group(1).replace(",", ""))


def get_death_rate_from_string(raw_str: str) -> Optional[float]:
    if m := re.search(r"(\d{1,3}(?:\.\d+)?) deaths", raw_str):
        return float(m.group(1)) / 1000
    return None


def get_rate_from_str(raw_str: str, search_term: str, denominator: int = 1) -> Optional[float]:
    pattern = re.compile(rf"(\d{{1,3}}(?:\.\d+)?) {search_term}")
    if m := re.search(pattern, raw_str):
        return float(m.group(1)) / denominator
    return None


def get_electricity_from_str(raw_str: str) -> Optional[float]:
    if m := re.search(r"((?:\d{1,3},?)+(?:\.\d+))\s(\w+)\skWh", raw_str):
        return convert_str_to_float(
            f"{m.group(1).replace(',', '')} {m.group(2)}"
        )
    return None


def get_boundary_countries_from_str(raw_str: str) -> Optional[List[str]]:
    if m := re.findall(r"(\w[\w ]+) (?:(?:\d{1,3},?)+(?:\.\d+)?) km", raw_str):
        return m
    return None


def get_elevations_from_str(raw_str: str) -> Optional[dict[str, float]]:
    elevations = {}
    elevation_labels = [
        "highest_elevation",
        "lowest_elevation",
        "mean_elvation",
    ]
    if m := re.findall(r"((?:\d{1,3},?)+(?:\.\d+)?) m", raw_str):
        for i, elevation in enumerate(m):
            if i > len(elevation_labels) - 1:
                break
            elevations[elevation_labels[i]] = elevation.replace(",", "")
        return elevations
    return None


def get_area_from_str(raw_str: str) -> Optional[float]:
    if m := re.search(r"((?:\d{1,3},?)+(?:\.\d+)?) sq km", raw_str):
        return float(m.group(1).replace(",", ""))
    return None


def get_population_from_str(raw_str: str) -> Optional[float]:
    if m := re.search(r"((?:\d{1,3},?)+(?:\.\d+)?)", raw_str):
        return int(m.group(1).replace(",", ""))


def get_dependency_ratios_from_str(raw_str: str, suffix: str = "", denominator: int = 100) -> Optional[dict[str, float]]:
    if m := re.findall(r"(\w[\w ]+):\s(\d{1,3}\.?\d?)", raw_str):
        return {x[0] + suffix: float(x[1]) / denominator for x in m}
    return None


def get_median_ages_from_str(raw_str: str) -> Optional[dict[str, float]]:
    if m := re.findall(r"(\w[\w ]+):\s(\d{1,3}\.?\d?) years", raw_str):
        return {x[0] + "_median_age": float(x[1]) for x in m}
    return None


def get_births_from_str(raw_str: str) -> Optional[float]:
    if m := re.search(r"(\d{1,3}\.?\d?) births", raw_str):
        return float(m.group(1)) / 1000
    return None


def find_div_by_string(soup: BeautifulSoup, div_name: str):
    tag = soup.find("h3", class_="mt30", string=div_name)
    if tag is None:
        return None
    tag = tag.find_parent("div")
    return tag.find("p")


def get_net_migration_from_str(raw_str: str) -> Optional[float]:
    if m := re.search(r"(-?\d{1,3}\.?\d?) migrant", raw_str):
        return float(m.group(1))


def get_rates_from_str(raw_str: str, suffix: str = "", denominator: int = 1000) -> Optional[dict]:
    if m := re.findall(r"(\w[\w ]+):\s(\d{1,3}\.?\d?)", raw_str):
        return {x[0] + suffix: float(x[1]) / denominator for x in m}
    return None


def get_infant_mortality_rates_from_str(raw_str: str) -> Optional[dict]:
    if m := re.findall(r"(\w[\w\s]+):\s(\d{1,3}\.?\d{0,3}) deaths/1,000 live births", raw_str):
        return {x[0] + "_infant_mortality": float(x[1]) / 1000 for x in m}
    return None

def get_percentages_from_str(raw_str: str) -> Optional[dict[str, float]]:
    if m := re.findall(r"(\w[\w ]+):\s(\d{1,3}\.?\d{0,3})%", raw_str):
        return {x[0]: float(x[1]) / 100 for x in m}
    return None
