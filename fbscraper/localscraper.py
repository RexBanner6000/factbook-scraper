from fbscraper.scrapers import CIAScraper
from bs4 import BeautifulSoup
import pandas as pd
from fbscraper.field_maps import original_field_map, later_field_map


class CIALocalScraper(CIAScraper):
    def __init__(self, base_url: str, field_maps: dict, year: int):
        super().__init__(year=year)
        self.base_url = base_url
        self.field_maps = field_maps

    def get_factbook_df(self):
        with open(self.base_url + "index.html", "r") as fp:
            soup = BeautifulSoup(fp, "html.parser")
            factbook_df = self.get_countries(soup)

        with open(self.base_url + f"fields/{self.field_maps['growth_rates']}.html", "r") as fp:
            soup = BeautifulSoup(fp, "html.parser")
            growth = self.get_population_growth_rate(soup)
            factbook_df = factbook_df.join(growth, how="outer")

        with open(self.base_url + f"fields/{self.field_maps['purchasing_power_parity']}.html", "r") as fp:
            soup = BeautifulSoup(fp, "html.parser")
            purchasing_power_parity = self.get_purchasing_power_parity(soup)
            factbook_df = factbook_df.join(purchasing_power_parity, how="outer")


        return factbook_df


if __name__ == "__main__":
    scraper = CIALocalScraper(
        base_url="./data/factbook-2002/",
        field_maps=original_field_map,
        year=2002
    )
    factbook_df = scraper.get_factbook_df()
    print("Factbook 2002")
    print(factbook_df.head())

    scraper = CIALocalScraper(
        base_url="./data/factbook-2019/",
        field_maps=later_field_map,
        year=2019
    )
    factbook_df = scraper.get_factbook_df()
    print("Factbook 2019")
    print(factbook_df.head())
