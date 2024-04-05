from bs4 import BeautifulSoup

from fbscraper import utils


def find_div_by_string(soup: BeautifulSoup, div_name: str):
    tag = soup.find("h3", class_="mt30", string=div_name)
    if tag is None:
        return None
    tag = tag.find_parent("div")
    return tag.find("p")


def get_areas_from_web(soup: BeautifulSoup):
    if para := find_div_by_string(soup, "Area"):
        areas = utils.get_areas_from_str(para.get_text())
        return areas
    return None


def get_coastline_from_web(soup: BeautifulSoup):
    if para := find_div_by_string(soup, "Coastline"):
        return {"coastline": utils.get_distance_from_str(para.get_text())}
    return None


def get_terrain(soup: BeautifulSoup):
    if para := find_div_by_string(soup, "Terrain"):
        return {"terrain": para.get_text()}
    return None


def get_climate(soup: BeautifulSoup):
    if para := find_div_by_string(soup, "Climate"):
        return {"climate": para.get_text()}


def get_border_countries(soup: BeautifulSoup):
    if para := find_div_by_string(soup, "Land boundaries"):
        return {
            "border_countries": utils.get_boundary_countries_from_str(
                para.get_text()
            )
        }
    return None


def get_elevation(soup: BeautifulSoup):
    if para := find_div_by_string(soup, "Elevation"):
        return utils.get_elevations_from_str(para.get_text())
