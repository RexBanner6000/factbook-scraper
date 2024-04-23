from bs4 import BeautifulSoup
from fbscraper import utils
import numpy as np


def get_areas_from_archive(soup: BeautifulSoup):
    areas = {}
    if para := utils.find_div_by_id(soup, "field-area"):
        subfields = utils.get_subfields(para)
        for key, value in subfields.items():
            areas[key + "_area"] = utils.get_area_from_str(value)
        return areas
    return None


def get_coastline_from_archive(soup: BeautifulSoup):
    if para := utils.find_div_by_id(soup, "field-coastline"):
        value = para.find("span", "subfield-number")
        if value is None:
            coastline_length = 0
        else:
            coastline_length = utils.get_distance_from_str(value.get_text())
        return {"coastline": coastline_length}
    return None


def get_terrain_from_archive(soup: BeautifulSoup):
    if para := utils.find_div_by_id(soup, "field-terrain"):
        return {
            "terrain": para.find("div", class_="category_data subfield text").get_text().strip()
        }
    return None


def get_climate_from_archive(soup: BeautifulSoup):
    if para := utils.find_div_by_id(soup, "field-climate"):
        return {
            "climate": para.find("div", class_="category_data subfield text").get_text().strip()
        }
    return None


def get_border_countries_from_archive(soup: BeautifulSoup):
    if para := utils.find_div_by_id(soup, "field-land-boundaries"):
        if border_countries_subfield := para.find("div", class_="category_data subfield text"):
            border_countries_str = border_countries_subfield.get_text()
            return {
                "border_countries": utils.get_boundary_countries_from_str(
                    border_countries_str
                )
            }
    return None


def get_elevation_from_archive(soup: BeautifulSoup):
    elevations = {}
    if para := utils.find_div_by_id(soup, "field-elevation"):
        subfields = utils.get_subfields(para)
        for key, value in subfields.items():
            elevations[key] = utils.get_elevation_from_str(value)
        return elevations
    return None


def get_irrigated_land_from_archive(soup: BeautifulSoup):
    if para := utils.find_div_by_id(soup, "field-irrigated-land"):
        if value := para.find("span", "subfield-number"):
            return {"irrigated_land": utils.get_area_from_str(value.get_text())}
    return None


def get_population_from_archive(soup: BeautifulSoup):
    if para := utils.find_div_by_id(soup, "field-population"):
        if value := para.find("span", "subfield-number"):
            return {"population": float(value.get_text().replace(",", ""))}
    return None


def get_age_structures_from_archive(soup: BeautifulSoup):
    age_structures = {}
    if para := utils.find_div_by_id(soup, "field-age-structure"):
        subfields = utils.get_subfields(para)
        for key, value in subfields.items():
            age_structures[key] = utils.get_percentage_from_string(value)
        return age_structures
    return None


def get_dependency_ratios_from_archive(soup: BeautifulSoup):
    dependency_ratios = {}
    if para := utils.find_div_by_id(soup, "field-dependency-ratios"):
        subfields = utils.get_subfields(para)
        for key, value in subfields.items():
            dependency_ratios[key] = float(value) / 100
        return dependency_ratios
    return None


def get_median_ages_from_archive(soup: BeautifulSoup):
    median_ages = {}
    if para := utils.find_div_by_id(soup, "field-median-age"):
        subfields = utils.get_subfields(para)
        for key, value in subfields.items():
            median_ages[key + "_median_age"] = utils.get_age_from_str(value)
        return median_ages
    return None


def get_population_growth_rate_from_archive(soup: BeautifulSoup):
    if para := utils.find_div_by_id(soup, "field-population-growth-rate"):
        if value := para.find("span", "subfield-number"):
            return {
                "population_growth_rate": utils.get_percentage_from_string(value.get_text())
            }
    return None


def get_birth_rate_from_archive(soup: BeautifulSoup):
    if para := utils.find_div_by_id(soup, "field-birth-rate"):
        if value := para.find("span", "subfield-number"):
            return {
                "birth_rate": utils.get_births_from_str(value.get_text())
            }
    return None


def get_death_rate_from_archive(soup: BeautifulSoup):
    if para := utils.find_div_by_id(soup, "field-death-rate"):
        if value := para.find("span", "subfield-number"):
            return {
                "death_rate": utils.get_death_rate_from_string(value.get_text())
            }
    return None


def get_net_migration_rate(soup: BeautifulSoup):
    if para := utils.find_div_by_id(soup, "field-net-migration-rate"):
        if value := para.find("span", "subfield-number"):
            return {
                "migration_rate": utils.get_net_migration_from_str(value.get_text())
            }
        return None


def get_urbanisation_from_archive(soup: BeautifulSoup):
    if para := utils.find_div_by_id(soup, "field-urbanization"):
        return utils.get_percentages_from_str(para.get_text())
    return None


def get_infant_mortality_from_archive(soup: BeautifulSoup):
    if para := utils.find_div_by_id(soup, "field-infant-mortality-rate"):
        return utils.get_infant_mortality_rates_from_str(para.get_text())
    return None


def get_life_expectancy_at_birth(soup: BeautifulSoup):
    if para := utils.find_div_by_id(soup, "field-life-expectancy-at-birth"):
        if life_expectancies := utils.get_rates_from_str(
                para.get_text(), suffix="_life_expectancy", denominator=1
        ):
            return life_expectancies
    return None


def get_total_fertility_rate_from_archive(soup: BeautifulSoup):
    if para := utils.find_div_by_id(soup, "field-total-fertility-rate"):
        return {"fertility_rate": utils.get_rate_from_str(para.get_text(), search_term="children born")}
    return None


def get_current_health_expenditure_from_archive(soup: BeautifulSoup):
    if para := utils.find_div_by_id(soup, "field-current-health-expenditure"):
        return {"health_expenditure": utils.get_percentage_from_string(para.get_text())}
    return None


def get_physicians_density_from_archive(soup: BeautifulSoup):
    if para := utils.find_div_by_id(soup, "field-physicians-density"):
        return {
            "physicians_density": utils.get_rate_from_str(
                para.get_text(), search_term="physicians", denominator=1000
            )
        }
    return None


def get_hospital_bed_density_from_archive(soup: BeautifulSoup):
    if para := utils.find_div_by_id(soup, "field-hospital-bed-density"):
        return {
            "hospital_bed_density": utils.get_rate_from_str(
                para.get_text(), search_term="beds", denominator=1000
            )
        }
    return None
