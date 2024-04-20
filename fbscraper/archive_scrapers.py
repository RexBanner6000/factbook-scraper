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


def get_dependency_ratios(soup: BeautifulSoup):
    dependency_ratios = {}
    if para := utils.find_div_by_id(soup, "field-dependency-ratios"):
        subfields = utils.get_subfields(para)
        for key, value in subfields.items():
            dependency_ratios[key] = float(value) / 100
        return dependency_ratios
    return None
