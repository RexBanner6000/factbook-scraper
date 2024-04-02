from bs4 import BeautifulSoup
import re


class CountryRecord:
    def __init__(
        self,
        country_name: str,
        country_code: str,
        base_path: str
    ):
        self.country_name = country_name
        self.country_code = country_code
        self.country_path = f"{base_path}{country_code}.html"
        self.population = None

    def scrape_population(self):
        with open(self.country_path, "r") as fp:
            soup = BeautifulSoup(fp, "html.parser")

        divs = soup.find_all("div")
        for div in divs:
            if re.match("Population:", div.get_text()):
                table_row = div.find_parent("tr")
                raw_str = table_row.find_all("td")[-1].get_text()
                if match := re.search(r"((\d{1,3},?)+)", raw_str):
                    self.population = int(match.group(0).replace(",", ""))


class CIALocalScraper:
    def __init__(
        self,
        index_html_path: str,
    ):
        self.index_html_path = index_html_path + "index.html"
        self.geos_path = index_html_path + "geos/"

    def get_countries(self):
        country_records = []
        with open(self.index_html_path, "r") as fp:
            soup = BeautifulSoup(fp, "html.parser")
        options = soup.find_all("option")
        for tag in options:
            if re.search("select a country", tag.text.lower()) or re.search("world", tag.text.lower()):
                continue
            country_records.append(
                CountryRecord(
                    country_name=tag.text.lstrip(),
                    country_code=tag.get("value")[5:7],
                    base_path=self.geos_path
                )
            )
        return country_records


if __name__ == "__main__":
    scraper = CIALocalScraper(index_html_path="./data/factbook-2002/")
    countries = scraper.get_countries()
    for country in countries:
        country.scrape_population()
        print(f"{country.country_name}: {country.population}")
