from bs4 import BeautifulSoup
from fbscraper import utils


def get_areas_from_web(soup: BeautifulSoup):
    tag = soup.find("h3", class_="mt30", string="Area")
    tag = tag.find_parent("div")
    para = tag.find("p")
    areas = utils.get_areas_from_str(para.get_text())
    return areas


def get_coastline_from_web(soup: BeautifulSoup):
    tag = soup.find("h3", class_="mt30", string="Coastline")
    tag = tag.find_parent("div")
    para = tag.find("p")
    return {"coastline": utils.get_distance_from_str(para.get_text())}
