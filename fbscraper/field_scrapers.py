from bs4 import BeautifulSoup

from fbscraper import utils
from typing import Optional


def get_areas_from_web(soup: BeautifulSoup):
    if para := utils.find_div_by_string(soup, "Area"):
        areas = utils.get_areas_from_str(para.get_text())
        return areas
    return None


def get_coastline_from_web(soup: BeautifulSoup):
    if para := utils.find_div_by_string(soup, "Coastline"):
        return {"coastline": utils.get_distance_from_str(para.get_text())}
    return None


def get_terrain(soup: BeautifulSoup):
    if para := utils.find_div_by_string(soup, "Terrain"):
        return {"terrain": para.get_text()}
    return None


def get_climate(soup: BeautifulSoup):
    if para := utils.find_div_by_string(soup, "Climate"):
        return {"climate": para.get_text()}


def get_border_countries(soup: BeautifulSoup):
    if para := utils.find_div_by_string(soup, "Land boundaries"):
        return {
            "border_countries": utils.get_boundary_countries_from_str(
                para.get_text()
            )
        }
    return None


def get_elevation(soup: BeautifulSoup):
    if para := utils.find_div_by_string(soup, "Elevation"):
        return utils.get_elevations_from_str(para.get_text())
    return None


def get_irrigated_land(soup: BeautifulSoup):
    if para := utils.find_div_by_string(soup, "Irrigated land"):
        return {"irrigated_land": utils.get_area_from_str(para.get_text())}
    return None


def get_population(soup: BeautifulSoup):
    if para := utils.find_div_by_string(soup, "Population"):
        return {"population": utils.get_population_from_str(para.get_text())}
    return None


def get_age_structures(soup: BeautifulSoup):
    if para := utils.find_div_by_string(soup, "Age structure"):
        return utils.get_age_structures(para.get_text())
    return None


def get_dependency_ratios(soup: BeautifulSoup):
    if para := utils.find_div_by_string(soup, "Dependency ratios"):
        return utils.get_dependency_ratios_from_str(para.get_text())
    return None


def get_median_ages(soup: BeautifulSoup):
    if para := utils.find_div_by_string(soup, "Median age"):
        return utils.get_median_ages_from_str(para.get_text())
    return None


def get_population_growth_rate(soup: BeautifulSoup) -> Optional[dict]:
    if para := utils.find_div_by_string(soup, "Population growth rate"):
        return {"population_growth_rate": utils.get_percentage_from_string(para.get_text())}
    return None


def get_birth_rate(soup: BeautifulSoup) -> Optional[dict]:
    if para := utils.find_div_by_string(soup, "Birth rate"):
        return {"birth_rate": utils.get_births_from_str(para.get_text())}
    return None


def get_death_rate(soup: BeautifulSoup) -> Optional[dict]:
    if para := utils.find_div_by_string(soup, "Death rate"):
        return {"death_rate": utils.get_death_rate_from_string(para.get_text())}
    return None
