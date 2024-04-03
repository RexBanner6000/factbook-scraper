from bs4 import BeautifulSoup
import pandas as pd
import re

from utils import get_dollar_string, convert_str_to_float


class CIALocalScraper:
    def __init__(
        self,
        base_url: str,
    ):
        self.base_url = base_url

    def get_purchasing_power_parity(self):
        with open(self.base_url + "fields/2001.html", "r") as fp:
            soup = BeautifulSoup(fp, "html.parser")
        table_rows = [x.find_parent("tr") for x in soup.find_all(string=re.compile(r"\$"))]
        countries = []
        gdps = []
        for row in table_rows:
            if row is None:
                continue
            cells = row.find_all("td")
            if gdp_str := get_dollar_string(cells[1].get_text()):
                countries.append(cells[0].get_text().replace("\n", ""))
                gdps.append(convert_str_to_float(gdp_str))
        return pd.Series(gdps, index=countries)

    def get_population_growth_rate(self):
        with open(self.base_url + "fields/2002.html", "r") as fp:
            soup = BeautifulSoup(fp, "html.parser")
        table_rows = [x.find_parent("tr") for x in soup.find_all(string=re.compile("%"))]
        countries = []
        growth_rates = []
        for row in table_rows:
            cells = row.find_all("td")
            if growth_str := re.match(r"(\d+(?:\.\d+))", cells[1].get_text()):
                countries.append(cells[0].get_text().replace("\n", ""))
                growth_rates.append(float(growth_str))
        return pd.Series(growth_rates, index=countries)


if __name__ == "__main__":
    scraper = CIALocalScraper(base_url="./data/factbook-2017/")
    print(scraper.get_purchasing_power_parity())
