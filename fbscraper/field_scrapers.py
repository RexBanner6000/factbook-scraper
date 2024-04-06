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


def get_net_migration_rate(soup: BeautifulSoup) -> Optional[dict]:
    if para := utils.find_div_by_string(soup, "Net migration rate"):
        return {"net_migration": utils.get_net_migration_from_str(para.get_text())}
    return None


def get_urbanisation(soup: BeautifulSoup) -> Optional[dict]:
    if para := utils.find_div_by_string(soup, "Urbanization"):
        return utils.get_percentages_from_str(para.get_text())
    return None


def get_infant_mortality(soup: BeautifulSoup) -> Optional[dict]:
    if para := utils.find_div_by_string(soup, "Infant mortality rate"):
        return utils.get_infant_mortality_rates_from_str(para.get_text())
    return None


def get_life_expectancy_at_birth(soup: BeautifulSoup) -> Optional[dict]:
    if para := utils.find_div_by_string(soup, "Life expectancy at birth"):
        life_expectancies = utils.get_rates_from_str(para.get_text(), suffix="_life_expectancy", denominator=1)
        for key in life_expectancies.keys():
            life_expectancies[key.replace("years", "")] = life_expectancies.pop(key)
        return life_expectancies
    return None


def get_total_fertility_rate(soup: BeautifulSoup) -> Optional[dict]:
    if para := utils.find_div_by_string(soup, "Total fertility rate"):
        return {"fertility_rate": utils.get_rate_from_str(para.get_text(), search_term="children born")}
    return None


def get_current_health_expenditure(soup: BeautifulSoup) -> Optional[dict]:
    if para := utils.find_div_by_string(soup, "Current health expenditure"):
        return {"health_expenditure": utils.get_percentage_from_string(para.get_text())}
    return None


def get_physicians_density(soup: BeautifulSoup) -> Optional[dict]:
    if para := utils.find_div_by_string(soup, "Physicians density"):
        return {
            "physicians_density": utils.get_rate_from_str(
                para.get_text(), search_term="physicians", denominator=1000
            )
        }
    return None


def get_hospital_bed_density(soup: BeautifulSoup) -> Optional[dict]:
    if para := utils.find_div_by_string(soup, "Hospital bed density"):
        return {
            "hospital_bed_density": utils.get_rate_from_str(
                para.get_text(), search_term="beds", denominator=1000
            )
        }
    return None


def get_total_alcohol_per_capita(soup: BeautifulSoup) -> Optional[dict]:
    if para := utils.find_div_by_string(soup, "Alcohol consumption per capita"):
        alcohol_consumption = utils.get_rates_from_str(para.get_text(), suffix="_litres_of_alcohol", denominator=1)
        return {"alcohol_per_capita": alcohol_consumption["total_litres_of_alcohol"]}
    return None


def get_tobacco_use_total(soup: BeautifulSoup) -> Optional[dict]:
    if para := utils.find_div_by_string(soup, "Tobacco use"):
        tobacco_use = utils.get_percentages_from_str(para.get_text())
        return {"tobacco_use_ratio": tobacco_use["total"]}
    return None
