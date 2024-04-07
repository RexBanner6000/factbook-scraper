from fbscraper.country_scraper import CIAScraper, field_scrapers
import pandas as pd

if __name__ == "__main__":
    scraper = CIAScraper(
        countries_url="https://www.cia.gov/the-world-factbook/about/archives/2021/field/country-name/",
        year=2021,
    )
    print("Scraping 2021...")
    scraper.get_country_codes(tag="h2", class_="h3")
    scraper.scrape_countries(field_scrapers)
    factbook_df = pd.DataFrame.from_dict(scraper.countries, orient="index")

    scraper = CIAScraper(
        countries_url="https://www.cia.gov/the-world-factbook/about/archives/2022/field/country-name/",
        year=2022,
    )
    print("Scraping 2022...")
    scraper.get_country_codes(tag="h2", class_="h3")
    scraper.scrape_countries(field_scrapers)
    factbook_df = pd.concat(
        [factbook_df, pd.DataFrame.from_dict(scraper.countries, orient="index")]
    )

    scraper = CIAScraper(
        countries_url="https://www.cia.gov/the-world-factbook/about/archives/2023/field/country-name/",
        year=2023,
    )
    print("Scraping 2023...")
    scraper.get_country_codes(tag="h3", class_="mt10")
    scraper.scrape_countries(field_scrapers)
    factbook_df = pd.concat(
        [factbook_df, pd.DataFrame.from_dict(scraper.countries, orient="index")]
    )

    scraper = CIAScraper(
        countries_url="https://www.cia.gov/the-world-factbook/field/country-name/",
        year=2024,
    )
    print("Scraping 2024...")
    scraper.get_country_codes()
    scraper.scrape_countries(field_scrapers)
    factbook_df = pd.concat(
        [factbook_df, pd.DataFrame.from_dict(scraper.countries, orient="index")]
    )
    print(factbook_df)
    factbook_df.to_csv("web_factbook_archives.csv")
