#!/usr/bin/env python3
"""
Download demographic data for all countries from World Bank Open Data API.
Generates JSON files for the Pyramidle game.

Data source: World Bank Open Data API
- Most recent available data (typically 2022-2023)
- Age/sex population pyramids
- Fertility, mortality, and birth indicators

Requirements:
    pip install requests
"""

import json
import os
import time
import requests
from typing import Dict, List, Optional, Tuple
from pathlib import Path

# World Bank API endpoint
WB_API_BASE = "https://api.worldbank.org/v2"

# Age groups for population pyramid
AGE_GROUPS = [
    '0-4', '5-9', '10-14', '15-19', '20-24', '25-29',
    '30-34', '35-39', '40-44', '45-49', '50-54', '55-59',
    '60-64', '65-69', '70-74', '75-79', '80-84', '85+'
]

# World Bank age group indicators (age-sex)
WB_AGE_INDICATORS = {
    '0-4': ('SP.POP.0004.MA', 'SP.POP.0004.FE'),
    '5-9': ('SP.POP.0509.MA', 'SP.POP.0509.FE'),
    '10-14': ('SP.POP.1014.MA', 'SP.POP.1014.FE'),
    '15-19': ('SP.POP.1519.MA', 'SP.POP.1519.FE'),
    '20-24': ('SP.POP.2024.MA', 'SP.POP.2024.FE'),
    '25-29': ('SP.POP.2529.MA', 'SP.POP.2529.FE'),
    '30-34': ('SP.POP.3034.MA', 'SP.POP.3034.FE'),
    '35-39': ('SP.POP.3539.MA', 'SP.POP.3539.FE'),
    '40-44': ('SP.POP.4044.MA', 'SP.POP.4044.FE'),
    '45-49': ('SP.POP.4549.MA', 'SP.POP.4549.FE'),
    '50-54': ('SP.POP.5054.MA', 'SP.POP.5054.FE'),
    '55-59': ('SP.POP.5559.MA', 'SP.POP.5559.FE'),
    '60-64': ('SP.POP.6064.MA', 'SP.POP.6064.FE'),
    '65-69': ('SP.POP.6569.MA', 'SP.POP.6569.FE'),
    '70-74': ('SP.POP.7074.MA', 'SP.POP.7074.FE'),
    '75-79': ('SP.POP.7579.MA', 'SP.POP.7579.FE'),
    '80+': ('SP.POP.80UP.MA', 'SP.POP.80UP.FE'),  # Will split into 80-84 and 85+
}

def get_wb_countries() -> List[Dict]:
    """Get list of countries from World Bank API."""
    print("Fetching country list from World Bank API...")
    url = f"{WB_API_BASE}/country?format=json&per_page=300"

    response = requests.get(url)
    response.raise_for_status()
    data = response.json()

    # World Bank returns [metadata, data]
    if len(data) < 2:
        raise Exception("Unexpected World Bank API response format")

    countries_data = data[1]

    # Filter for actual countries (not aggregates/regions)
    countries = []
    for country in countries_data:
        # Exclude aggregates and regions
        if country.get('region', {}).get('id') != 'NA':  # NA = Not applicable (aggregates)
            # Only include countries with ISO3 codes
            if country.get('id') and len(country.get('id', '')) == 3:
                countries.append({
                    'code': country['id'],
                    'name': country['name'],
                })

    print(f"Found {len(countries)} countries")
    return countries

def fetch_indicator_data(country_code: str, indicator: str, year: int = 2022) -> Optional[float]:
    """
    Fetch a single indicator value for a country.
    Tries multiple recent years if specified year not available.
    """
    # Try last 5 years if data not available for specified year
    for y in range(year, year - 5, -1):
        url = f"{WB_API_BASE}/country/{country_code}/indicator/{indicator}?format=json&date={y}"

        try:
            response = requests.get(url)
            response.raise_for_status()
            data = response.json()

            if len(data) > 1 and data[1]:
                for record in data[1]:
                    if record.get('value') is not None:
                        return float(record['value'])

            time.sleep(0.05)  # Small delay to avoid rate limiting

        except Exception as e:
            continue

    return None

def get_population_pyramid(country_code: str) -> Optional[Dict]:
    """
    Get population pyramid data from World Bank.
    Returns dict with male/female age group populations and total.
    """
    print(f"  Fetching age/sex data for {country_code}...")

    pyramid = {
        'male': {},
        'female': {}
    }

    total_pop = 0
    missing_groups = []

    # Fetch all age groups
    for age_group, (male_indicator, female_indicator) in WB_AGE_INDICATORS.items():
        male_value = fetch_indicator_data(country_code, male_indicator)
        female_value = fetch_indicator_data(country_code, female_indicator)

        if male_value is None or female_value is None:
            missing_groups.append(age_group)
            continue

        # Handle the 80+ group - split into 80-84 and 85+
        if age_group == '80+':
            # Approximate split: 60% in 80-84, 40% in 85+
            male_80_84 = int(male_value * 0.6)
            male_85_plus = int(male_value * 0.4)
            female_80_84 = int(female_value * 0.6)
            female_85_plus = int(female_value * 0.4)

            pyramid['male']['80-84'] = male_80_84
            pyramid['male']['85+'] = male_85_plus
            pyramid['female']['80-84'] = female_80_84
            pyramid['female']['85+'] = female_85_plus

            total_pop += int(male_value + female_value)
        else:
            pyramid['male'][age_group] = int(male_value)
            pyramid['female'][age_group] = int(female_value)
            total_pop += int(male_value + female_value)

    # Check if we have enough data
    if len(missing_groups) > 5:  # Too many missing groups
        print(f"  Warning: {country_code} missing {len(missing_groups)} age groups")
        return None

    # Fill in missing groups with 0
    for age_group in AGE_GROUPS:
        if age_group not in pyramid['male']:
            pyramid['male'][age_group] = 0
        if age_group not in pyramid['female']:
            pyramid['female'][age_group] = 0

    return {
        'pyramid': pyramid,
        'population': total_pop
    }

def calculate_median_age(pyramid: Dict) -> float:
    """
    Calculate approximate median age from population pyramid.
    Uses midpoint of age groups weighted by population.
    """
    age_midpoints = {
        '0-4': 2, '5-9': 7, '10-14': 12, '15-19': 17, '20-24': 22, '25-29': 27,
        '30-34': 32, '35-39': 37, '40-44': 42, '45-49': 47, '50-54': 52, '55-59': 57,
        '60-64': 62, '65-69': 67, '70-74': 72, '75-79': 77, '80-84': 82, '85+': 87
    }

    total_pop = 0
    weighted_sum = 0

    for age_group in AGE_GROUPS:
        male_pop = pyramid['male'].get(age_group, 0)
        female_pop = pyramid['female'].get(age_group, 0)
        pop = male_pop + female_pop

        total_pop += pop
        weighted_sum += pop * age_midpoints[age_group]

    if total_pop == 0:
        return 30.0  # Default

    return weighted_sum / total_pop

def get_year_births_peaked(country_code: str) -> int:
    """
    Find year with highest births by looking at crude birth rate
    multiplied by population over time.
    """
    print(f"  Fetching historical births for {country_code}...")

    # Fetch historical CBR and population data
    cbr_url = f"{WB_API_BASE}/country/{country_code}/indicator/SP.DYN.CBRT.IN?format=json&date=1960:2023&per_page=100"
    pop_url = f"{WB_API_BASE}/country/{country_code}/indicator/SP.POP.TOTL?format=json&date=1960:2023&per_page=100"

    try:
        cbr_response = requests.get(cbr_url)
        pop_response = requests.get(pop_url)

        cbr_data = cbr_response.json()[1] if len(cbr_response.json()) > 1 else []
        pop_data = pop_response.json()[1] if len(pop_response.json()) > 1 else []

        if not cbr_data or not pop_data:
            return 2000  # Default

        # Create dictionaries for easy lookup
        cbr_by_year = {d['date']: d['value'] for d in cbr_data if d.get('value')}
        pop_by_year = {d['date']: d['value'] for d in pop_data if d.get('value')}

        # Calculate births for each year
        births_by_year = {}
        for year in cbr_by_year:
            if year in pop_by_year:
                # CBR is per 1,000, so divide by 1000
                births = (cbr_by_year[year] / 1000) * pop_by_year[year]
                births_by_year[year] = births

        if not births_by_year:
            return 2000

        # Find year with max births
        max_year = max(births_by_year, key=births_by_year.get)
        return int(max_year)

    except Exception as e:
        print(f"  Warning: Could not calculate births peak for {country_code}: {e}")
        return 2000

def create_country_data(country: Dict) -> Optional[Dict]:
    """Create complete country data JSON from World Bank data."""
    code = country['code']
    name = country['name']

    print(f"\nProcessing {name} ({code})...")

    # Get population pyramid
    pyramid_data = get_population_pyramid(code)
    if not pyramid_data:
        print(f"  Skipping {code}: Insufficient population data")
        return None

    # Get demographic indicators
    print(f"  Fetching demographic indicators for {code}...")
    tfr = fetch_indicator_data(code, 'SP.DYN.TFRT.IN')
    life_exp = fetch_indicator_data(code, 'SP.DYN.LE00.IN')
    cbr = fetch_indicator_data(code, 'SP.DYN.CBRT.IN')

    # Calculate median age from pyramid
    median_age = calculate_median_age(pyramid_data['pyramid'])

    # Get year births peaked
    year_births_peaked = get_year_births_peaked(code)

    # Use defaults if indicators missing
    if tfr is None:
        print(f"  Warning: {code} missing TFR, using default")
        tfr = 2.1
    if life_exp is None:
        print(f"  Warning: {code} missing life expectancy, using default")
        life_exp = 70.0
    if cbr is None:
        print(f"  Warning: {code} missing CBR, using default")
        cbr = 20.0

    country_data = {
        'code': code,
        'name': name,
        'population': pyramid_data['population'],
        'totalFertilityRate': round(tfr, 2),
        'medianAge': round(median_age, 1),
        'yearBirthsPeaked': year_births_peaked,
        'lifeExpectancy': round(life_exp, 1),
        'crudeBirthRate': round(cbr, 1),
        'pyramid': pyramid_data['pyramid']
    }

    return country_data

def main():
    """Main function to download all country data."""
    print("=" * 60)
    print("Pyramidle Data Downloader (World Bank API)")
    print("=" * 60)

    # Create output directories
    output_dir = Path("public/data/countries")
    output_dir.mkdir(parents=True, exist_ok=True)

    # Get list of countries
    countries = get_wb_countries()

    # Country list for countries.json
    country_list = []

    # Process each country
    successful = 0
    failed = 0

    for country in countries:
        try:
            country_data = create_country_data(country)

            if country_data:
                # Save individual country file
                code = country_data['code']
                output_file = output_dir / f"{code}.json"

                with open(output_file, 'w', encoding='utf-8') as f:
                    json.dump(country_data, f, indent=2, ensure_ascii=False)

                # Add to country list
                country_list.append({
                    'code': code,
                    'name': country_data['name']
                })

                successful += 1
                print(f"  ✓ Saved {code}.json")
            else:
                failed += 1

            # Rate limiting - be nice to the API
            time.sleep(0.3)

        except Exception as e:
            print(f"  ✗ Error processing {country.get('code')}: {e}")
            failed += 1

    # Sort country list by code
    country_list.sort(key=lambda x: x['code'])

    # Save country list
    countries_file = Path("public/data/countries.json")
    with open(countries_file, 'w', encoding='utf-8') as f:
        json.dump(country_list, f, indent=2, ensure_ascii=False)

    print("\n" + "=" * 60)
    print(f"Download complete!")
    print(f"  Successful: {successful}")
    print(f"  Failed: {failed}")
    print(f"  Total countries in list: {len(country_list)}")
    print(f"\nFiles saved to: {output_dir.absolute()}")
    print(f"Country list saved to: {countries_file.absolute()}")
    print("=" * 60)

if __name__ == "__main__":
    main()
