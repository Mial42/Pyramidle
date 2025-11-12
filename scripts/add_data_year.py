#!/usr/bin/env python3
"""
Add dataYear field to existing country JSON files by checking World Bank API
for the actual year of the demographic data.

This is a lightweight script that makes only 1 API call per country to determine
the data year, without re-downloading all the demographic data.

Requirements:
    pip install requests
"""

import json
import requests
import time
from pathlib import Path
from typing import Optional

# World Bank API
WB_API_BASE = "https://api.worldbank.org/v2"

# HTTP headers
HEADERS = {
    'User-Agent': 'Pyramidle/1.0 (Educational Project)',
    'Accept': 'application/json'
}

def get_data_year(country_code: str) -> Optional[int]:
    """
    Check what year the population data is from for a given country.
    Uses total population indicator as a proxy for all demographic data.
    """
    # Use total population as indicator (same data year as pyramid data)
    indicator = "SP.POP.TOTL"
    url = f"{WB_API_BASE}/country/{country_code}/indicator/{indicator}?format=json&date=2015:2024&per_page=10"

    try:
        response = requests.get(url, headers=HEADERS, timeout=10)
        response.raise_for_status()
        data = response.json()

        if len(data) > 1 and data[1]:
            # Data is sorted by year descending (most recent first)
            for record in data[1]:
                if record.get('value') is not None:
                    year = int(record['date'])
                    return year

        time.sleep(0.1)  # Rate limiting

    except Exception as e:
        print(f"  Error checking data year for {country_code}: {e}")

    return None

def add_data_year_to_file(json_path: Path) -> bool:
    """Add dataYear field to a country JSON file."""
    try:
        # Read existing data
        with open(json_path, 'r') as f:
            data = json.load(f)

        country_code = data['code']
        country_name = data['name']

        # Check if dataYear already exists
        if 'dataYear' in data:
            print(f"  {country_name}: Already has dataYear = {data['dataYear']}")
            return True

        # Get the data year from API
        print(f"  {country_name}: Checking data year...", end=" ")
        data_year = get_data_year(country_code)

        if data_year is None:
            print("Could not determine year")
            return False

        # Add dataYear field (after code and name)
        new_data = {
            'code': data['code'],
            'name': data['name'],
            'dataYear': data_year,
        }

        # Add remaining fields
        for key, value in data.items():
            if key not in ['code', 'name']:
                new_data[key] = value

        # Save updated file
        with open(json_path, 'w') as f:
            json.dump(new_data, f, indent=2)

        print(f"{data_year}")
        return True

    except Exception as e:
        print(f"  Error updating {json_path}: {e}")
        return False

def main():
    """Main function to add dataYear field to all country JSON files."""
    print("=" * 60)
    print("Pyramidle: Add Data Year Field")
    print("=" * 60)
    print()

    # Find country JSON files
    countries_dir = Path(__file__).parent.parent / 'public' / 'data' / 'countries'

    if not countries_dir.exists():
        print(f"Error: Countries directory not found at {countries_dir}")
        return

    json_files = sorted(list(countries_dir.glob('*.json')))
    print(f"Found {len(json_files)} country JSON files")
    print()

    # Process each country
    updated_count = 0
    failed_count = 0

    for json_file in json_files:
        if add_data_year_to_file(json_file):
            updated_count += 1
        else:
            failed_count += 1

    print()
    print("=" * 60)
    print(f"Updated: {updated_count} countries")
    print(f"Failed: {failed_count} countries")
    print("=" * 60)

if __name__ == '__main__':
    main()
