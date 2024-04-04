from fbscraper.scrapers import CIAScraper
from bs4 import BeautifulSoup
import pandas as pd


class CIALocalScraper(CIAScraper):
    def __init__(self, base_url: str):
        self.base_url = base_url

    def get_factbook_df(self):
        with open(self.base_url + "fields/2002.html", "r") as fp:
            soup = BeautifulSoup(fp, "html.parser")
            growth = pd.DataFrame.from_dict(
                self.get_population_growth_rate(soup), orient="index", columns=["growth"]
            )

        with open(self.base_url + "fields/2001.html", "r") as fp:
            soup = BeautifulSoup(fp, "html.parser")
            purchasing_power_parity = pd.DataFrame.from_dict(
                self.get_purchasing_power_parity(soup), orient="index", columns=["purchasing_power_parity"]
            )

        factbook_df = purchasing_power_parity.join(growth, how="outer")
        return factbook_df


if __name__ == "__main__":
    scraper = CIALocalScraper(base_url="./data/factbook-2002/")
    factbook_df = scraper.get_factbook_df()
    print(factbook_df.head())
