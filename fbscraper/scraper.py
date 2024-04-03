from bs4 import BeautifulSoup
import pandas as pd
import re


class CIALocalScraper:
    def __init__(
        self,
        base_url: str,
    ):
        self.base_url = base_url

    def get_purchasing_power_parity(self):
        with open(self.base_url + "fields/2001.html", "r") as fp:
            soup = BeautifulSoup(fp, "html.parser")
        table_rows = [x.find_parent("tr") for x in soup.find_all(string=re.compile("purchasing power parity"))]
        countries = []
        gdps = []
        for row in table_rows:
            cells = row.find_all("td")
            if gdp_str := re.findall(r"(?:\$(\d+ \w+))", cells[1].get_text()):
                countries.append(cells[0].get_text().replace("\n", ""))
                gdps.append(gdp_str[0])
        return pd.Series(gdps, index=countries)


if __name__ == "__main__":
    scraper = CIALocalScraper(base_url="./data/factbook-2002/")
    print(scraper.get_purchasing_power_parity())
