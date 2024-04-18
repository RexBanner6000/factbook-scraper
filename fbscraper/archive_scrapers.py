from bs4 import BeautifulSoup
from fbscraper import utils


def get_areas_from_web(soup: BeautifulSoup):
    areas = {}
    if para := utils.find_div_by_id(soup, "field-area"):
        subfields = utils.get_subfields(para)
        for key, value in subfields.items():
            areas[key + "_area"] = utils.get_area_from_str(value)
        return areas
    return None
