import re
from typing import List, Optional
from bs4 import BeautifulSoup


def get_dollar_string(raw_str: str) -> Optional[float]:
    if m := re.search(r"\$((?:\d{1,3},?)+(?:\.\d+)?)\s?(\w+)?", raw_str):
        if m.group(2) is None or m.group(2) == "note":
            return float(m.group(1).replace(",", ""))
        else:
            return convert_str_to_float(m.group(1) + " " + m.group(2))
    return None


def convert_str_to_float(number_str: str) -> float:
    multipliers = {
        "thousand": 1000,
        "million": 1_000_000,
        "billion": 1_000_000_000,
        "trillion": 1_000_000_000_000,
    }
    string_split = number_str.split(" ")
    if not re.search(rf"{'|'.join(multipliers.keys())}", number_str):
        return float(string_split[0].replace(",", ""))
    return float(string_split[0]) * multipliers[string_split[1]]


def get_percentage_from_string(raw_str: str) -> Optional[float]:
    if m := re.search(r"(-?\d+(?:\.\d+)?)%", raw_str):
        return float(m.group(1)) / 100
    return None


def get_country_name(raw_str: str) -> Optional[str]:
    if m := re.search(r"\w[\w ]+", raw_str):
        return m.group(0).rstrip()
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


def get_boundary_countries_from_str(raw_str: str) -> Optional[List[str]]:
    if m := re.findall(r"(\w[\w ]+) (?:(?:\d{1,3},?)+(?:\.\d+)?) km", raw_str):
        return m
    return None


def get_elevations_from_str(raw_str: str) -> Optional[dict[str, float]]:
    #TODO: Fix this
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
    if m := re.search(r"^((?:\d{1,3},?)+(?:\.\d+)?)(\s\w+)?", raw_str):
        if m.group(2) is None:
            return int(m.group(1).replace(",", ""))
        else:
            return convert_str_to_float(m.group(1) + " " + m.group(2).replace(" ", ""))
    return None


def get_dependency_ratios_from_str(raw_str: str, suffix: str = "", denominator: int = 100) -> Optional[dict[str, float]]:
    if m := re.findall(r"(\w[\w ]+):\s(\d{1,3}\.?\d?|NA)", raw_str):
        dependency_ratios = {}
        for match in m:
            if match[1] == "NA":
                dependency_ratios[match[0] + suffix] = None
            else:
                dependency_ratios[match[0] + suffix] = float(match[1]) / denominator
        return dependency_ratios
    return None


def get_age_from_str(raw_str: str) -> Optional[str]:
    if m := re.search(r"(\d{1,3}\.?\d?) years", raw_str):
        return float(m.group(1).replace(",", ""))
    return None


def get_median_ages_from_str(raw_str: str) -> Optional[dict[str, float]]:
    if m := re.findall(r"(\w[\w ]+):\s(\d{1,3}\.?\d?) years", raw_str):
        return {x[0] + "_median_age": float(x[1]) for x in m}
    return None


def get_births_from_str(raw_str: str) -> Optional[float]:
    if m := re.search(r"(\d{1,3}\.?\d?) births", raw_str):
        return float(m.group(1)) / 1000
    return None


def find_div_by_h3_string(soup: BeautifulSoup, div_name: str):
    tag = soup.find("h3", class_="mt30", string=div_name)
    if tag is None:
        return None
    tag = tag.find_parent("div")
    return tag.find("p")


def find_div_by_id(soup: BeautifulSoup, div_id: str):
    return soup.find("div", id=div_id)


def get_net_migration_from_str(raw_str: str) -> Optional[float]:
    if m := re.search(r"(-?\d{1,3}\.?\d?) migrant", raw_str):
        return float(m.group(1))


def get_rates_from_str(raw_str: str, suffix: str = "", denominator: int = 1000) -> Optional[dict]:
    if m := re.findall(r"(\w[\w ]+):\s(\d{1,3}(?:\.\d+)?)", raw_str):
        return {x[0] + suffix: float(x[1]) / denominator for x in m}
    return None


def get_infant_mortality_rates_from_str(raw_str: str) -> Optional[dict]:
    if m := re.findall(r"(\w[\w\s]+):\s(\d{1,3}\.?\d{0,3}) deaths/1,000 live births", raw_str):
        return {x[0] + "_infant_mortality": float(x[1]) / 1000 for x in m}
    return None


def get_percentages_from_str(raw_str: str, suffix: str = "") -> Optional[dict[str, float]]:
    if m := re.findall(r"(\w+):\s(\d{1,3}\.?\d{0,3}|NA)%?", raw_str):
        percentages = {}
        for match in m:
            if match[1] == "NA":
                percentages[match[0] + suffix] = None
            else:
                percentages[match[0] + suffix] = float(match[1]) / 100
        return percentages
    return None


def get_subfields(soup: BeautifulSoup):
    subfields = {}
    subfield_name_tags = soup.find_all("span", "subfield-name")
    subfield_value_tags = soup.find_all("span", "subfield-number")

    for name_tag, value_tag in zip(subfield_name_tags, subfield_value_tags):
        subfields[name_tag.get_text().rstrip(":")] = value_tag.get_text()

    return subfields


def get_elevation_from_str(raw_str: str):
    if m := re.search(r"((?:\d{1,3},?)+(?:\.\d+)?) m", raw_str):
        return float(m.group(1).replace(",", ""))
    return None


def get_category_data_from_category(soup: BeautifulSoup, category_pattern: str):
    if category_header := soup.find("a", string=re.compile(category_pattern)):
        return category_header.find_parent("tr").find_next("tr")
    return None


def get_field_by_name(soup: BeautifulSoup, name: str):
    fields = soup.find_all("div", id="field")
    header = [div for div in fields if name in div.get_text()]
    if header is not None:
        return header[0].find_next("div")
    return None
