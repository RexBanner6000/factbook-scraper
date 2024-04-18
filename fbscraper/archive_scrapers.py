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


def get_terrain(soup: BeautifulSoup):
    if para := utils.find_div_by_id(soup, "field-terrain"):
        return {
            "terrain": para.find("div", class_="category_data subfield text").get_text().strip()
        }
    return None


def get_climate(soup: BeautifulSoup):
    if para := utils.find_div_by_id(soup, "field-climate"):
        return {
            "climate": para.find("div", class_="category_data subfield text").get_text().strip()
        }
    return None
