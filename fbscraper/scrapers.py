import re

import pandas as pd
from bs4 import BeautifulSoup
from utils import (
    convert_str_to_float,
    get_dollar_string,
    get_percentage_from_string,
    get_country_name,
    get_age_structures,
    get_areas_from_str,
    get_distance_from_str
)


class CIAScraper:
    def __init__(self, year: int):
        self.year = year

    def get_countries(self, soup: BeautifulSoup) -> pd.DataFrame:
        options = soup.find_all("option")
        countries = []
        for tag in options:
            if re.search(r"select a country", tag.text.lower()):
                continue
            countries.append(get_country_name(tag.text))
        countries_df = pd.DataFrame(index=countries)
        countries_df["year"] = self.year
        return countries_df

    @staticmethod
    def get_purchasing_power_parity(soup: BeautifulSoup) -> pd.DataFrame:
        table_rows = get_table_rows(soup, re.compile(r"\$"))
        purchasing_power_parity = {}
        for row in table_rows:
            if row is None:
                continue
            cells = row.find_all("td")
            if gdp_str := get_dollar_string(cells[1].get_text()):
                purchasing_power_parity[
                    get_country_name(cells[0].get_text())
                ] = convert_str_to_float(gdp_str)

        return pd.DataFrame.from_dict(
            purchasing_power_parity, orient="index", columns=["purchasing_power_parity"]
        )

    @staticmethod
    def get_population_growth_rate(soup: BeautifulSoup) -> pd.DataFrame:
        table_rows = get_table_rows(soup, re.compile(r"\d%"))
        growth_rates = {}
        for row in table_rows:
            cells = row.find_all("td")
            if growth_prc := get_percentage_from_string(cells[1].get_text()):
                growth_rates[get_country_name(cells[0].get_text())] = growth_prc
        return pd.DataFrame.from_dict(
            growth_rates, orient="index", columns=["growth"]
        )

    @staticmethod
    def get_age_structure(soup: BeautifulSoup) -> pd.DataFrame:
        table_rows = get_table_rows(soup, re.compile(r"\d%"))
        age_structures = {}
        for row in table_rows:
            cells = row.find_all("td")
            if age_structure := get_age_structures(cells[1].get_text()):
                age_structures[get_country_name(cells[0].get_text())] = age_structure
        return pd.DataFrame.from_dict(age_structures, orient="index")

    @staticmethod
    def get_areas(soup: BeautifulSoup) -> pd.DataFrame:
        table_rows = get_table_rows(soup, re.compile(r"sq km"))
        areas = {}
        for row in table_rows:
            cells = row.find_all("td")
            if area := get_areas_from_str(cells[1].get_text()):
                areas[get_country_name(cells[0].get_text())] = area

        return pd.DataFrame.from_dict(areas, orient="index")

    @staticmethod
    def get_coastline(soup: BeautifulSoup) -> pd.DataFrame:
        table_rows = get_table_rows(soup, re.compile(r"km"))
        coastlines = {}
        for row in table_rows:
            if row is None:
                continue
            cells = row.find_all("td")
            coastline = get_distance_from_str(cells[1].get_text())
            if coastline is not None:
                coastlines[get_country_name(cells[0].get_text())] = coastline

        return pd.DataFrame.from_dict(coastlines, orient="index", columns=["coastline"])


def get_table_rows(soup: BeautifulSoup, pattern: re.Pattern):
    table_rows = [
        x.find_parent("tr")
        for x in soup.find_all(string=pattern)
    ]
    return table_rows
