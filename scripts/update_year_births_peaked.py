#!/usr/bin/env python3
"""
Download births data and update the yearBirthsPeaked field in country JSON files.

Data sources (tried in order):
1. Our World in Data CSV (UN World Population Prospects 2024)
2. UN World Population Prospects direct download
3. Local CSV file if provided

Usage:
    python update_year_births_peaked.py
    python update_year_births_peaked.py --file births_data.csv

Requirements:
    pip install requests pandas
"""

import json
import os
import sys
import argparse
import requests
import pandas as pd
from pathlib import Path
from typing import Dict, Optional

# Our World in Data CSV URLs for births data
OWID_URLS = [
    "https://ourworldindata.org/grapher/births-and-deaths-projected-to-2100.csv?v=1&csvType=full",
    "https://github.com/owid/owid-datasets/raw/master/datasets/UN%20WPP%20(2024)/UN%20WPP%20(2024).csv",
]

# UN World Population Prospects direct download
UN_WPP_BIRTHS_URL = "https://population.un.org/wpp/Download/Files/1_Indicators%20(Standard)/CSV_FILES/WPP2024_Demographic_Indicators_Medium.csv"

# HTTP headers
HEADERS = {
    'User-Agent': 'Pyramidle/1.0 (Educational Project)',
    'Accept': 'text/csv'
}

# Country code mapping (3-letter ISO to OWID names)
# Our World in Data sometimes uses different country names
COUNTRY_NAME_OVERRIDES = {
    'USA': 'United States',
    'GBR': 'United Kingdom',
    'RUS': 'Russia',
    'VNM': 'Vietnam',
    'KOR': 'South Korea',
    'PRK': 'North Korea',
    'SYR': 'Syria',
    'IRN': 'Iran',
    'VEN': 'Venezuela',
    'BOL': 'Bolivia',
    'TZA': 'Tanzania',
    'COD': 'Democratic Republic of Congo',
    'COG': 'Congo',
    'LAO': 'Laos',
    'MDA': 'Moldova',
    'TUR': 'Turkey',
    'PSE': 'Palestine',
}

def download_births_data(local_file: Optional[str] = None) -> pd.DataFrame:
    """
    Download births data CSV from various sources or load from local file.

    Args:
        local_file: Path to local CSV file if available

    Returns:
        DataFrame with births data
    """
    # If local file provided, use it
    if local_file:
        print(f"Loading births data from local file: {local_file}")
        df = pd.read_csv(local_file)
        print(f"Loaded {len(df)} rows from local file")
        print(f"Columns: {df.columns.tolist()}")
        return df

    # Try Our World in Data sources
    for i, url in enumerate(OWID_URLS, 1):
        print(f"Trying Our World in Data source {i}/{len(OWID_URLS)}...")
        print(f"  URL: {url}")
        try:
            response = requests.get(url, headers=HEADERS, timeout=60)
            response.raise_for_status()

            temp_file = f'/tmp/births_data_{i}.csv'
            with open(temp_file, 'wb') as f:
                f.write(response.content)

            df = pd.read_csv(temp_file)
            print(f"✓ Downloaded {len(df)} rows")
            print(f"  Columns: {', '.join(df.columns.tolist()[:5])}...")
            return df

        except Exception as e:
            print(f"✗ Failed: {e}")

    # Try UN World Population Prospects
    print("\nTrying UN World Population Prospects...")
    print(f"  URL: {UN_WPP_BIRTHS_URL}")
    try:
        response = requests.get(UN_WPP_BIRTHS_URL, headers=HEADERS, timeout=120)
        response.raise_for_status()

        temp_file = '/tmp/un_wpp_births.csv'
        with open(temp_file, 'wb') as f:
            f.write(response.content)

        df = pd.read_csv(temp_file)
        print(f"✓ Downloaded {len(df)} rows from UN WPP")
        print(f"  Columns: {', '.join(df.columns.tolist()[:5])}...")

        # UN WPP format: has columns like 'Births' (in thousands)
        return df

    except Exception as e:
        print(f"✗ Failed: {e}")

    raise Exception("Could not download births data from any source. Try downloading manually and using --file option.")

def find_year_births_peaked(df: pd.DataFrame, country_name: str, country_code: str) -> Optional[int]:
    """
    Find the year when births peaked for a given country.

    Args:
        df: DataFrame with births data
        country_name: Country name from JSON
        country_code: ISO 3-letter country code

    Returns:
        Year when births peaked, or None if not found
    """
    # Detect data format (OWID vs UN WPP)
    is_un_wpp = 'Location' in df.columns or 'LocID' in df.columns
    is_owid = 'Entity' in df.columns

    # Check if we have an override for this country code
    search_name = COUNTRY_NAME_OVERRIDES.get(country_code, country_name)

    # Filter data for this country based on format
    country_data = pd.DataFrame()

    if is_owid:
        # OWID format: Entity, Code, Year columns
        country_data = df[df['Entity'] == search_name].copy()

        if len(country_data) == 0 and search_name != country_name:
            country_data = df[df['Entity'] == country_name].copy()

        if len(country_data) == 0 and 'Code' in df.columns:
            country_data = df[df['Code'] == country_code].copy()

    elif is_un_wpp:
        # UN WPP format: Location, ISO3_code, Time columns
        if 'ISO3_code' in df.columns:
            country_data = df[df['ISO3_code'] == country_code].copy()

        if len(country_data) == 0 and 'Location' in df.columns:
            country_data = df[df['Location'] == country_name].copy()

            if len(country_data) == 0 and search_name != country_name:
                country_data = df[df['Location'] == search_name].copy()

    if len(country_data) == 0:
        print(f"  Warning: No data found for {country_name} ({country_code})")
        return None

    # Find the births column
    births_col = None
    year_col = 'Year' if 'Year' in df.columns else 'Time'

    # Look for births column
    for col in df.columns:
        col_lower = col.lower()
        if col_lower == 'births' or 'live birth' in col_lower or 'number of births' in col_lower:
            births_col = col
            break

    if births_col is None:
        print(f"  Warning: Could not find births column. Columns: {df.columns.tolist()}")
        return None

    # Filter to historical data only (before 2025)
    if year_col in country_data.columns:
        country_data = country_data[country_data[year_col] < 2025].copy()

    # Remove rows with missing births data
    country_data = country_data[country_data[births_col].notna()].copy()

    if len(country_data) == 0:
        print(f"  Warning: No historical births data for {country_name}")
        return None

    # Find year with maximum births
    max_idx = country_data[births_col].idxmax()
    peak_year = int(country_data.loc[max_idx, year_col])
    peak_births = country_data.loc[max_idx, births_col]

    # UN WPP births are in thousands
    if is_un_wpp:
        peak_births *= 1000

    print(f"  {country_name}: Births peaked in {peak_year} with {peak_births:,.0f} births")

    return peak_year

def update_country_json(json_path: Path, year_peaked: int) -> bool:
    """Update the yearBirthsPeaked field in a country JSON file."""
    try:
        with open(json_path, 'r') as f:
            data = json.load(f)

        old_year = data.get('yearBirthsPeaked', 'unknown')
        data['yearBirthsPeaked'] = year_peaked

        with open(json_path, 'w') as f:
            json.dump(data, f, indent=2)

        if old_year != year_peaked:
            print(f"  Updated {json_path.name}: {old_year} -> {year_peaked}")

        return True

    except Exception as e:
        print(f"  Error updating {json_path}: {e}")
        return False

def main():
    """Main function to update all country JSON files with correct birth peak years."""
    parser = argparse.ArgumentParser(
        description='Update yearBirthsPeaked field in country JSON files using births data'
    )
    parser.add_argument(
        '--file',
        type=str,
        help='Path to local CSV file with births data (optional)'
    )
    args = parser.parse_args()

    print("=" * 60)
    print("Pyramidle: Update Year Births Peaked")
    print("=" * 60)
    print()

    # Download or load births data
    try:
        df = download_births_data(local_file=args.file)
        print()
    except Exception as e:
        print(f"\n✗ Failed to get births data: {e}")
        print("\nTo download data manually:")
        print("1. Visit: https://ourworldindata.org/grapher/births-and-deaths-projected-to-2100")
        print("2. Click 'Download' and save CSV")
        print("3. Run: python update_year_births_peaked.py --file <path-to-csv>")
        return

    # Find country JSON files
    countries_dir = Path(__file__).parent.parent / 'public' / 'data' / 'countries'

    if not countries_dir.exists():
        print(f"Error: Countries directory not found at {countries_dir}")
        return

    json_files = list(countries_dir.glob('*.json'))
    print(f"\nFound {len(json_files)} country JSON files")
    print()

    # Process each country
    updated_count = 0
    not_found_count = 0

    for json_file in sorted(json_files):
        # Read country data
        with open(json_file, 'r') as f:
            country_data = json.load(f)

        country_name = country_data['name']
        country_code = country_data['code']

        print(f"Processing {country_name} ({country_code})...")

        # Find year births peaked
        year_peaked = find_year_births_peaked(df, country_name, country_code)

        if year_peaked is not None:
            if update_country_json(json_file, year_peaked):
                updated_count += 1
        else:
            not_found_count += 1

    print()
    print("=" * 60)
    print(f"Updated: {updated_count} countries")
    print(f"Not found: {not_found_count} countries")
    print("=" * 60)

if __name__ == '__main__':
    main()
