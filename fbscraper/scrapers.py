import re

import pandas as pd
from bs4 import BeautifulSoup
from utils import (
    convert_str_to_float,
    get_dollar_string,
    get_percentage_from_string,
    get_country_name
)


#TODO: make a separate class for each website format type that generates a BeautifulSoup object and pass to each of these functions
class CIAScraper:
    def get_purchasing_power_parity(self, soup: BeautifulSoup) -> dict[str, float]:
        with open(self.base_url + "fields/2001.html", "r") as fp:
            soup = BeautifulSoup(fp, "html.parser")
        table_rows = [
            x.find_parent("tr")
            for x in soup.find_all(string=re.compile(r"\$"))
        ]
        purchasing_power_parity = {}
        for row in table_rows:
            if row is None:
                continue
            cells = row.find_all("td")
            if gdp_str := get_dollar_string(cells[1].get_text()):
                purchasing_power_parity[
                    get_country_name(cells[0].get_text())
                ] = convert_str_to_float(gdp_str)
        return purchasing_power_parity

    def get_population_growth_rate(self, soup: BeautifulSoup):
        with open(self.base_url + "fields/2002.html", "r") as fp:
            soup = BeautifulSoup(fp, "html.parser")
        table_rows = [
            x.find_parent("tr")
            for x in soup.find_all(string=re.compile(r"\d%"))
        ]
        growth_rates = {}
        for row in table_rows:
            cells = row.find_all("td")
            if growth_prc := get_percentage_from_string(cells[1].get_text()):
                growth_rates[get_country_name(cells[0].get_text())] = growth_prc
        return growth_rates
