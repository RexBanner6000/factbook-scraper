import re
from typing import Callable, List

import pandas as pd
import requests
from bs4 import BeautifulSoup
from inspect import getmembers, isfunction
from fbscraper import field_scrapers
from fbscraper.utils import get_country_name


field_scrapers = [x[1]for x in getmembers(field_scrapers, isfunction)]


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
                "link": "https://www.cia.gov" + tag.a["href"]
            }

    def scrape_countries(self, field_scrapers: List[Callable]):
        for country, data in self.countries.items():
            if "American Samoa" in country:
                break
            print(f"Scraping {country}...")
            soup = self.make_scraper(data["link"])
            for field_scraper in field_scrapers:
                new_fields = field_scraper(soup)
                if new_fields is not None:
                    data.update(new_fields)


if __name__ == "__main__":
    scraper = CIAScraper(
        countries_url="https://www.cia.gov/the-world-factbook/field/country-name/",
        year=2024,
    )
    scraper.get_country_codes()
    scraper.scrape_countries(field_scrapers)
    factbook_2024_df = pd.DataFrame.from_dict(scraper.countries, orient="index")
    print(factbook_2024_df.head())

    scraper = CIAScraper(
        countries_url="https://www.cia.gov/the-world-factbook/about/archives/2021/field/country-name/",
        year=2021,
    )
    scraper.get_country_codes(tag="h2", class_="h3")
    scraper.scrape_countries(field_scrapers)
    factbook_2021_df = pd.DataFrame.from_dict(scraper.countries, orient="index")
    print(factbook_2021_df.head())
