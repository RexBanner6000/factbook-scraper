from fbscraper.country_scraper import CIAArchiveScraper, field_scrapers
import pandas as pd

if __name__ == "__main__":
    factbook_df = pd.DataFrame()
    previous_countries = set()
    for year in range(2009, 2021):
        field = 2142 if year < 2018 else 296
        scraper = CIAArchiveScraper(
            countries_path=f"S:/datasets/cia-world-factbook/factbook-{year}/fields/{field}.html",
            geos_path=f"S:/datasets/cia-world-factbook/factbook-{year}/geos/",
            year=year
        )
        print(f"Scraping {year}...")
        try:
            scraper.get_country_codes()
            scraper.scrape_countries(field_scrapers)
            factbook_df = pd.concat(
                [factbook_df, pd.DataFrame.from_dict(scraper.countries, orient="index")]
            )
            year_countries = set(factbook_df[factbook_df["year"] == year].index)
            print(f"Finished {year}!")
            new_countries = year_countries - previous_countries
            print(f"\tNew countries: {len(new_countries)}")
            print(f"\t\t - {new_countries}")
            previous_countries = year_countries
        except Exception as e:
            print("Unexpected error")
            print(e)

    factbook_df.to_csv("offline_factbook_archives.csv")
