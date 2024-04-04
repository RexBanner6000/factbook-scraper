import re

import pandas as pd
from bs4 import BeautifulSoup
from utils import (
    convert_str_to_float,
    get_dollar_string,
    get_percentage_from_string,
)


class CIALocalScraper:
    def __init__(
        self,
        base_url: str,
    ):
        self.base_url = base_url

    def get_factbook_df(self) -> pd.DataFrame:
        purchasing_power_parity = pd.DataFrame.from_dict(
            self.get_purchasing_power_parity(), orient="index", columns=["purchasing_power_parity"]
        )
        growth = pd.DataFrame.from_dict(
            self.get_population_growth_rate(), orient="index", columns=["growth"]
        )
        factbook_df = purchasing_power_parity.join(growth, how="outer")
        return factbook_df

    def get_purchasing_power_parity(self) -> dict[str, float]:
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
                    cells[0].get_text().replace("\n", "")
                ] = convert_str_to_float(gdp_str)
        return purchasing_power_parity

    def get_population_growth_rate(self):
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
                growth_rates[cells[0].get_text().replace("\n", "")] = growth_prc
        return growth_rates


if __name__ == "__main__":
    scraper = CIALocalScraper(base_url="./data/factbook-2017/")
    factbook_df = scraper.get_factbook_df()
