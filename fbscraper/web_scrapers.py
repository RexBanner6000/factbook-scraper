from bs4 import BeautifulSoup

from fbscraper import utils
from typing import Optional


def get_areas_from_web(soup: BeautifulSoup):
    if para := utils.find_div_by_h3_string(soup, "Area"):
        areas = utils.get_areas_from_str(para.get_text())
        return areas
    return None


def get_coastline_from_web(soup: BeautifulSoup):
    if para := utils.find_div_by_h3_string(soup, "Coastline"):
        return {"coastline": utils.get_distance_from_str(para.get_text())}
    return None


def get_terrain(soup: BeautifulSoup):
    if para := utils.find_div_by_h3_string(soup, "Terrain"):
        return {"terrain": para.get_text()}
    return None


def get_climate(soup: BeautifulSoup):
    if para := utils.find_div_by_h3_string(soup, "Climate"):
        return {"climate": para.get_text()}


def get_border_countries(soup: BeautifulSoup):
    if para := utils.find_div_by_h3_string(soup, "Land boundaries"):
        return {
            "border_countries": utils.get_boundary_countries_from_str(
                para.get_text()
            )
        }
    return None


def get_elevation(soup: BeautifulSoup):
    if para := utils.find_div_by_h3_string(soup, "Elevation"):
        return utils.get_elevations_from_str(para.get_text())
    return None


def get_irrigated_land(soup: BeautifulSoup):
    if para := utils.find_div_by_h3_string(soup, "Irrigated land"):
        return {"irrigated_land": utils.get_area_from_str(para.get_text())}
    return None


def get_population(soup: BeautifulSoup):
    if para := utils.find_div_by_h3_string(soup, "Population"):
        return {"population": utils.get_population_from_str(para.get_text())}
    return None


def get_age_structures(soup: BeautifulSoup):
    if para := utils.find_div_by_h3_string(soup, "Age structure"):
        return utils.get_age_structures(para.get_text())
    return None


def get_dependency_ratios(soup: BeautifulSoup):
    if para := utils.find_div_by_h3_string(soup, "Dependency ratios"):
        return utils.get_dependency_ratios_from_str(para.get_text())
    return None


def get_median_ages(soup: BeautifulSoup):
    if para := utils.find_div_by_h3_string(soup, "Median age"):
        return utils.get_median_ages_from_str(para.get_text())
    return None


def get_population_growth_rate(soup: BeautifulSoup) -> Optional[dict]:
    if para := utils.find_div_by_h3_string(soup, "Population growth rate"):
        return {"population_growth_rate": utils.get_percentage_from_string(para.get_text())}
    return None


def get_birth_rate(soup: BeautifulSoup) -> Optional[dict]:
    if para := utils.find_div_by_h3_string(soup, "Birth rate"):
        return {"birth_rate": utils.get_births_from_str(para.get_text())}
    return None


def get_death_rate(soup: BeautifulSoup) -> Optional[dict]:
    if para := utils.find_div_by_h3_string(soup, "Death rate"):
        return {"death_rate": utils.get_death_rate_from_string(para.get_text())}
    return None


def get_net_migration_rate(soup: BeautifulSoup) -> Optional[dict]:
    if para := utils.find_div_by_h3_string(soup, "Net migration rate"):
        return {"net_migration": utils.get_net_migration_from_str(para.get_text())}
    return None


def get_urbanisation(soup: BeautifulSoup) -> Optional[dict]:
    if para := utils.find_div_by_h3_string(soup, "Urbanization"):
        return utils.get_percentages_from_str(para.get_text())
    return None


def get_infant_mortality(soup: BeautifulSoup) -> Optional[dict]:
    if para := utils.find_div_by_h3_string(soup, "Infant mortality rate"):
        return utils.get_infant_mortality_rates_from_str(para.get_text())
    return None


def get_life_expectancy_at_birth(soup: BeautifulSoup) -> Optional[dict]:
    if para := utils.find_div_by_h3_string(soup, "Life expectancy at birth"):
        if life_expectancies := utils.get_rates_from_str(
                para.get_text(), suffix="_life_expectancy", denominator=1
        ):
            keys = [x for x in life_expectancies.keys()]
            for key in keys:
                life_expectancies[key.replace("years", "")] = life_expectancies.pop(key)
            return life_expectancies
    return None


def get_total_fertility_rate(soup: BeautifulSoup) -> Optional[dict]:
    if para := utils.find_div_by_h3_string(soup, "Total fertility rate"):
        return {"fertility_rate": utils.get_rate_from_str(para.get_text(), search_term="children born")}
    return None


def get_current_health_expenditure(soup: BeautifulSoup) -> Optional[dict]:
    if para := utils.find_div_by_h3_string(soup, "Current health expenditure"):
        return {"health_expenditure": utils.get_percentage_from_string(para.get_text())}
    return None


def get_physicians_density(soup: BeautifulSoup) -> Optional[dict]:
    if para := utils.find_div_by_h3_string(soup, "Physicians density"):
        return {
            "physicians_density": utils.get_rate_from_str(
                para.get_text(), search_term="physicians", denominator=1000
            )
        }
    return None


def get_hospital_bed_density(soup: BeautifulSoup) -> Optional[dict]:
    if para := utils.find_div_by_h3_string(soup, "Hospital bed density"):
        return {
            "hospital_bed_density": utils.get_rate_from_str(
                para.get_text(), search_term="beds", denominator=1000
            )
        }
    return None


def get_total_alcohol_per_capita(soup: BeautifulSoup) -> Optional[dict]:
    if para := utils.find_div_by_h3_string(soup, "Alcohol consumption per capita"):
        alcohol_consumption = utils.get_rates_from_str(para.get_text(), suffix="_litres_of_alcohol", denominator=1)
        return {"alcohol_per_capita": alcohol_consumption["total_litres_of_alcohol"]}
    return None


def get_tobacco_use_total(soup: BeautifulSoup) -> Optional[dict]:
    if para := utils.find_div_by_h3_string(soup, "Tobacco use"):
        tobacco_use = utils.get_percentages_from_str(para.get_text())
        return {"tobacco_use_ratio": tobacco_use["total"]}
    return None


def get_obesity_rate(soup: BeautifulSoup) -> Optional[dict]:
    if para := utils.find_div_by_h3_string(soup, "Obesity - adult prevalence rate"):
        return {
            "obesity_rate": utils.get_percentage_from_string(para.get_text())
        }
    return None


def get_children_under_weight(soup: BeautifulSoup) -> Optional[dict]:
    if para := utils.find_div_by_h3_string(soup, "Children under the age of 5 years underweight"):
        return {
            "child_under_weight": utils.get_percentage_from_string(para.get_text())
        }
    return None


def get_education_expenditures(soup: BeautifulSoup) -> Optional[dict]:
    if para := utils.find_div_by_h3_string(soup, "Education expenditures"):
        return {
            "education_expenditure": utils.get_percentage_from_string(para.get_text())
        }
    return None


def get_literacy_rates(soup: BeautifulSoup) -> Optional[dict]:
    if para := utils.find_div_by_h3_string(soup, "Literacy"):
        return utils.get_percentages_from_str(para.get_text(), suffix="_literacy")
    return None


def get_air_pollutants(soup: BeautifulSoup) -> Optional[dict]:
    if para := utils.find_div_by_h3_string(soup, "Air pollutants"):
        return utils.get_rates_from_str(para.get_text(), denominator=1)
    return None


def get_real_gdp(soup: BeautifulSoup) -> Optional[dict]:
    if para := utils.find_div_by_h3_string(soup, "Real GDP (purchasing power parity)"):
        return {
            "real_gdp": utils.get_dollar_string(para.get_text())
        }
    return None


def get_gdp_growth_rate(soup: BeautifulSoup) -> Optional[dict]:
    if para := utils.find_div_by_h3_string(soup, "Real GDP growth rate"):
        return {
            "gdp_growth": utils.get_percentage_from_string(para.get_text())
        }
    return None


def get_inflation_rate(soup: BeautifulSoup) -> Optional[dict]:
    if para := utils.find_div_by_h3_string(soup, "Inflation rate (consumer prices)"):
        return {
            "inflation_rate": utils.get_percentage_from_string(para.get_text())
        }
    return None


def get_gdp_composition(soup: BeautifulSoup) -> Optional[dict]:
    if para := utils.find_div_by_h3_string(soup, "GDP - composition, by sector of origin"):
        return utils.get_percentages_from_str(para.get_text(), suffix="_prc_gdp")
    return None


def get_industrial_production_growth_rate(soup: BeautifulSoup) -> Optional[dict]:
    if para := utils.find_div_by_h3_string(soup, "Industrial production growth rate"):
        return {
            "industrial_production_growth": utils.get_percentage_from_string(para.get_text())
        }
    return None


def get_unemployment_rate(soup: BeautifulSoup) -> Optional[dict]:
    if para := utils.find_div_by_h3_string(soup, "Unemployment rate"):
        return {
            "unemployment_rate": utils.get_percentage_from_string(para.get_text())
        }
    return None


def get_percentage_in_poverty(soup: BeautifulSoup) -> Optional[dict]:
    if para := utils.find_div_by_h3_string(soup, "Population below poverty line"):
        return {
            "poverty_rate": utils.get_percentage_from_string(para.get_text())
        }
    return None


def get_electricity_access(soup: BeautifulSoup) -> Optional[dict]:
    if para := utils.find_div_by_h3_string(soup, "Electricity access"):
        electricity_access = utils.get_percentages_from_str(para.get_text(), suffix="_electricity_access")
        return {
            "electricity_access": electricity_access["population_electricity_access"]
        }
    return None
