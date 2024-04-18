import re
from typing import Callable, List

import pandas as pd
import requests
from bs4 import BeautifulSoup
from inspect import getmembers, isfunction
from fbscraper import web_scrapers
from fbscraper.utils import get_country_name


field_scrapers = [x[1]for x in getmembers(web_scrapers, isfunction)]


class CIAScraper:
    def __init__(self, countries_url: str, year: int):
        self.countries_url = countries_url
        self.countries = {}
        self.year = year

    @staticmethod
    def make_scraper(url: str) -> BeautifulSoup:
        r = requests.get(url)
        return BeautifulSoup(r.content, "html.parser")

    def get_country_codes(self, tag: str = "h3", class_: str = "mt10"):
        soup = self.make_scraper(self.countries_url)
        links = soup.find_all(tag, class_=class_)
        for tag in links:
            if re.search(r"\sOcean\s?", tag.text):
                continue
            self.countries[get_country_name(tag.text)] = {
                "link": "https://www.cia.gov" + tag.a["href"],
                "year": self.year
            }

    def scrape_countries(self, field_scrapers: List[Callable]):
        for country, data in self.countries.items():
            print(f"Scraping {country}...")
            soup = self.make_scraper(data["link"])
            for field_scraper in field_scrapers:
                new_fields = field_scraper(soup)
                if new_fields is not None:
                    data.update(new_fields)

    def scrape_country_for_field(self, country_name: str, field_scraper: Callable):
        data = self.countries[country_name]
        soup = self.make_scraper(data["link"])
        return field_scraper(soup)


class CIAArchiveScraper:
    def __init__(self, countries_path: str, geos_path: str, year: int):
        self.countries_path = countries_path
        self.countries = {}
        self.year = year
        self.geos_path = geos_path

    def get_country_codes(self):
        with open(self.countries_path) as fp:
            soup = BeautifulSoup(fp, 'html.parser')
        links = soup.find_all("td", class_="country")
        for tag in links:
            if re.search(r"\sOcean\s?", tag.text):
                continue
            self.countries[get_country_name(tag.text)] = {
                "country_code": tag.a["href"][8:10],
                "link": self.geos_path + tag.a["href"][8:10] + ".html",
                "year": self.year
            }


if __name__ == "__main__":
    # scraper = CIAScraper(
    #     countries_url="https://www.cia.gov/the-world-factbook/about/archives/2023/field/country-name/",
    #     year=2023,
    # )
    # scraper.get_country_codes(tag="h3", class_="mt10")
    # new_field = scraper.scrape_country_for_field("Falkland Islands", web_scrapers.get_life_expectancy_at_birth)
    # print(new_field)

    scraper = CIAArchiveScraper(
        countries_path="S:/datasets/cia-world-factbook/factbook-2020/fields/296.html",
        geos_path="S:/datasets/cia-world-factbook/factbook-2020/geos/",
        year=2020
    )
    scraper.get_country_codes()
    print("Done!")
