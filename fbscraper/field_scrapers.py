from bs4 import BeautifulSoup
from fbscraper.utils import get_areas_from_str


def get_areas_from_web(soup: BeautifulSoup):
    tag = soup.find("h3", class_="mt30", string="Area")
    tag = tag.find_parent("div")
    para = tag.find("p")
    areas = get_areas_from_str(para.get_text())
    return areas
