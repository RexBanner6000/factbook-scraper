from typing import Callable, List

import pandas as pd
import requests
from bs4 import BeautifulSoup

from fbscraper.field_scrapers import (
    get_areas_from_web,
    get_border_countries,
    get_climate,
    get_coastline_from_web,
    get_terrain,
)
from fbscraper.utils import get_country_name

field_scrapers = [
    get_areas_from_web,
    get_coastline_from_web,
    get_terrain,
    get_border_countries,
    get_climate,
]


class CIAScraper:
    def __init__(self, countries_url: str, year: int):
        self.countries_url = countries_url
        self.countries = {}
        self.year = year

    @staticmethod
    def make_scraper(url: str) -> BeautifulSoup:
        r = requests.get(url)
        return BeautifulSoup(r.content, "html.parser")

    def get_country_codes(self):
        soup = self.make_scraper(self.countries_url)
        links = soup.find_all("h3", class_="mt10")
        for tag in links:
            self.countries[get_country_name(tag.text)] = {
                "link": "https://www.cia.gov" + tag.a["href"]
            }

    def scrape_countries(self, field_scrapers: List[Callable]):
        for country, data in self.countries.items():
            if "Argentina" in country:
                break
            print(f"Scraping {country}...")
            soup = self.make_scraper(data["link"])
            for field_scraper in field_scrapers:
                new_fields = field_scraper(soup)
                if new_fields is not None:
                    data.update(new_fields)


if __name__ == "__main__":
    scraper = CIAScraper(
        countries_url="https://www.cia.gov/the-world-factbook/about/archives/2023/field/country-name/",
        year=2024,
    )
    scraper.get_country_codes()
    scraper.scrape_countries(field_scrapers)
    factbook_df = pd.DataFrame.from_dict(scraper.countries, orient="index")
    print(factbook_df.head())
