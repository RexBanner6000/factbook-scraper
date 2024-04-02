from bs4 import BeautifulSoup
import re


class CIALocalScraper:
    def __init__(
        self,
        index_html_path: str,
    ):
        self.index_html_path = index_html_path

    def get_countries(self):
        countries = []
        with open(self.index_html_path, "r") as fp:
            soup = BeautifulSoup(fp, "html.parser")
            options = soup.find_all("option")
            for tag in options:
                if re.match("select a country", tag.text.lower()):
                    continue
                countries.append(tag.text)
        return countries


if __name__ == "__main__":
    scraper = CIALocalScraper(index_html_path="./data/factbook-2002/index.html")
    countries = scraper.get_countries()
    print(countries)
