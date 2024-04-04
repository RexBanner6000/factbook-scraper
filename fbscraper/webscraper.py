from fbscraper.scrapers import CIAScraper
from bs4 import BeautifulSoup
import pandas as pd
from fbscraper.field_maps import web_field_map
import requests


class CIAWebScraper(CIAScraper):
    def __init__(self, base_url: str, field_maps: dict):
        self.base_url = base_url
        self.field_maps = field_maps

    def get_factbook_df(self):
        r = requests.get(self.base_url + f"field/{web_field_map['growth_rates']}")
        soup = BeautifulSoup(r.content, "html.parser")
        growth = pd.DataFrame.from_dict(
            self.get_population_growth_rate(soup), orient="index", columns=["growth"]
        )

        r = requests.get(self.base_url + f"field/{web_field_map['purchasing_power_parity']}")
        soup = BeautifulSoup(r.content, "html.parser")
        purchasing_power_parity = pd.DataFrame.from_dict(
            self.get_purchasing_power_parity(soup), orient="index", columns=["purchasing_power_parity"]
        )

        factbook_df = purchasing_power_parity.join(growth, how="outer")
        return factbook_df


if __name__ == "__main__":
    scraper = CIAWebScraper(
        base_url="https://www.cia.gov/the-world-factbook/",
        field_maps=web_field_map
    )
    factbook_df = scraper.get_factbook_df()
    print("Factbook 2024")
    print(factbook_df.head())
