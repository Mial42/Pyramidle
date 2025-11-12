#!/usr/bin/env python3
"""
Download demographic data for all countries from UN and World Bank APIs.
Generates JSON files for the Pyramidle game.

Data sources:
- UN World Population Prospects 2022: Age/sex data, fertility, mortality
- World Bank Open Data: Additional indicators and validation

Requirements:
    pip install requests pandas
"""

import json
import os
import time
import requests
from typing import Dict, List, Optional
from pathlib import Path

# API endpoints
UN_API_BASE = "https://population.un.org/dataportalapi/api/v1"
WB_API_BASE = "https://api.worldbank.org/v2"

# Age groups for population pyramid
AGE_GROUPS = [
    '0-4', '5-9', '10-14', '15-19', '20-24', '25-29',
    '30-34', '35-39', '40-44', '45-49', '50-54', '55-59',
    '60-64', '65-69', '70-74', '75-79', '80-84', '85+'
]

def get_un_locations() -> List[Dict]:
    """Get list of countries from UN API."""
    print("Fetching country list from UN API...")
    url = f"{UN_API_BASE}/locations"
    response = requests.get(url)
    response.raise_for_status()
    data = response.json()

    # Filter for countries only (not regions or aggregates)
    # Check if location has iso3 code (only countries have this)
    countries = []
    for loc in data['data']:
        # Countries have iso3 codes, regions/aggregates typically don't
        if loc.get('iso3') and loc.get('iso3') != '':
            # Additional check: exclude if it's explicitly marked as a region
            loc_type = loc.get('locationType')
            if loc_type:
                # Type 4 = Country, but API structure may vary
                if isinstance(loc_type, dict):
                    if loc_type.get('id') == 4:
                        countries.append(loc)
                elif loc_type == 4:
                    countries.append(loc)
            else:
                # If no location type, include if it has iso3
                countries.append(loc)

    print(f"Found {len(countries)} countries")
    return countries

def get_population_by_age_sex(location_id: int, iso_code: str) -> Optional[Dict]:
    """
    Get population pyramid data from UN API.
    Returns dict with male/female age group populations.
    """
    print(f"  Fetching age/sex data for {iso_code}...")

    # UN API: Population by age and sex (indicator 47 = Population by 5-year age groups and sex)
    url = f"{UN_API_BASE}/data/indicators/47/locations/{location_id}/start/2022/end/2022"

    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()

        if 'data' not in data or len(data['data']) == 0:
            print(f"  Warning: No age/sex data for {iso_code}")
            return None

        pyramid = {
            'male': {},
            'female': {}
        }

        total_pop = 0

        for record in data['data']:
            age_label = record.get('ageLabel', '')
            sex = record.get('sex', '')
            value = record.get('value', 0)

            # Map UN age labels to our format
            age_group = map_age_label(age_label)

            if age_group and sex in ['Male', 'Female']:
                sex_key = sex.lower()
                # Value is in thousands, convert to actual population
                population = int(value * 1000)

                if age_group in pyramid[sex_key]:
                    pyramid[sex_key][age_group] += population
                else:
                    pyramid[sex_key][age_group] = population

                total_pop += population

        # Ensure all age groups are present
        for age_group in AGE_GROUPS:
            if age_group not in pyramid['male']:
                pyramid['male'][age_group] = 0
            if age_group not in pyramid['female']:
                pyramid['female'][age_group] = 0

        return {
            'pyramid': pyramid,
            'population': total_pop
        }

    except Exception as e:
        print(f"  Error fetching age/sex data for {iso_code}: {e}")
        return None

def map_age_label(un_label: str) -> Optional[str]:
    """Map UN age labels to our age group format."""
    # UN uses labels like "0-4", "5-9", ..., "100+"
    # We use the same except "85+" for 85 and above

    if not un_label:
        return None

    if un_label in AGE_GROUPS:
        return un_label

    # Handle 85+ and above age groups
    if un_label in ['85-89', '90-94', '95-99', '100+']:
        return '85+'

    return un_label if un_label in AGE_GROUPS else None

def get_demographic_indicators(location_id: int, iso_code: str) -> Dict:
    """Get TFR, life expectancy, median age from UN API."""
    print(f"  Fetching demographic indicators for {iso_code}...")

    indicators = {
        'totalFertilityRate': None,
        'lifeExpectancy': None,
        'medianAge': None,
    }

    # Indicator IDs:
    # 68 = Total fertility rate
    # 69 = Life expectancy at birth (both sexes)
    # 31 = Median age

    indicator_map = {
        68: 'totalFertilityRate',
        69: 'lifeExpectancy',
        31: 'medianAge',
    }

    for indicator_id, key in indicator_map.items():
        try:
            url = f"{UN_API_BASE}/data/indicators/{indicator_id}/locations/{location_id}/start/2022/end/2022"
            response = requests.get(url)
            response.raise_for_status()
            data = response.json()

            if 'data' in data and len(data['data']) > 0:
                # Get the most recent value
                value = data['data'][0].get('value')
                if value is not None:
                    indicators[key] = round(float(value), 2)

            time.sleep(0.1)  # Rate limiting

        except Exception as e:
            print(f"  Warning: Could not fetch indicator {indicator_id} for {iso_code}: {e}")

    return indicators

def get_births_data(location_id: int, iso_code: str) -> Optional[int]:
    """
    Get historical births data to find year births peaked.
    Returns the year with the highest number of births.
    """
    print(f"  Fetching births history for {iso_code}...")

    try:
        # Indicator 19 = Births
        url = f"{UN_API_BASE}/data/indicators/19/locations/{location_id}/start/1950/end/2022"
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()

        if 'data' not in data or len(data['data']) == 0:
            return None

        # Find year with maximum births
        max_births = 0
        max_year = None

        for record in data['data']:
            year = record.get('timeLabel')
            value = record.get('value', 0)

            if value > max_births:
                max_births = value
                max_year = int(year)

        return max_year

    except Exception as e:
        print(f"  Warning: Could not fetch births data for {iso_code}: {e}")
        return None

def get_crude_birth_rate(location_id: int, iso_code: str) -> Optional[float]:
    """Get crude birth rate from UN API."""
    print(f"  Fetching crude birth rate for {iso_code}...")

    try:
        # Indicator 21 = Crude birth rate
        url = f"{UN_API_BASE}/data/indicators/21/locations/{location_id}/start/2022/end/2022"
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()

        if 'data' in data and len(data['data']) > 0:
            value = data['data'][0].get('value')
            if value is not None:
                return round(float(value), 2)

        return None

    except Exception as e:
        print(f"  Warning: Could not fetch CBR for {iso_code}: {e}")
        return None

def create_country_data(location: Dict) -> Optional[Dict]:
    """Create complete country data JSON."""
    iso_code = location.get('iso3')
    name = location.get('name')
    location_id = location.get('id')

    if not iso_code or not name or not location_id:
        return None

    print(f"\nProcessing {name} ({iso_code})...")

    # Get population pyramid
    pop_data = get_population_by_age_sex(location_id, iso_code)
    if not pop_data:
        print(f"  Skipping {iso_code}: No population data available")
        return None

    # Get demographic indicators
    indicators = get_demographic_indicators(location_id, iso_code)

    # Get births peak year
    year_births_peaked = get_births_data(location_id, iso_code)

    # Get crude birth rate
    crude_birth_rate = get_crude_birth_rate(location_id, iso_code)

    # Check if we have all required data
    if not all([
        indicators.get('totalFertilityRate'),
        indicators.get('medianAge'),
        indicators.get('lifeExpectancy'),
        year_births_peaked,
        crude_birth_rate
    ]):
        print(f"  Warning: {iso_code} missing some indicators, using defaults where needed")

    country_data = {
        'code': iso_code,
        'name': name,
        'population': pop_data['population'],
        'totalFertilityRate': indicators.get('totalFertilityRate', 2.1),
        'medianAge': indicators.get('medianAge', 30.0),
        'yearBirthsPeaked': year_births_peaked or 2000,
        'lifeExpectancy': indicators.get('lifeExpectancy', 70.0),
        'crudeBirthRate': crude_birth_rate or 20.0,
        'pyramid': pop_data['pyramid']
    }

    return country_data

def main():
    """Main function to download all country data."""
    print("=" * 60)
    print("Pyramidle Data Downloader")
    print("=" * 60)

    # Create output directories
    output_dir = Path("public/data/countries")
    output_dir.mkdir(parents=True, exist_ok=True)

    # Get list of countries
    countries = get_un_locations()

    # Country list for countries.json
    country_list = []

    # Process each country
    successful = 0
    failed = 0

    for location in countries:
        try:
            country_data = create_country_data(location)

            if country_data:
                # Save individual country file
                iso_code = country_data['code']
                output_file = output_dir / f"{iso_code}.json"

                with open(output_file, 'w', encoding='utf-8') as f:
                    json.dump(country_data, f, indent=2, ensure_ascii=False)

                # Add to country list
                country_list.append({
                    'code': iso_code,
                    'name': country_data['name']
                })

                successful += 1
                print(f"  ✓ Saved {iso_code}.json")
            else:
                failed += 1

            # Rate limiting - be nice to the API
            time.sleep(0.5)

        except Exception as e:
            print(f"  ✗ Error processing {location.get('iso3')}: {e}")
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
