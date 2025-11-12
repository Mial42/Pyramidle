#!/usr/bin/env python3
"""
Fix country JSON files with missing or default values by retrying API calls.

Fixes:
- Age pyramid values that are 0 (missing data)
- yearBirthsPeaked that is 2000 (default fallback)

Only makes API calls for the specific missing values, not full re-download.

Requirements:
    pip install requests
"""

import json
import requests
import time
from pathlib import Path
from typing import Dict, Optional, List, Tuple

# World Bank API
WB_API_BASE = "https://api.worldbank.org/v2"

# HTTP headers
HEADERS = {
    'User-Agent': 'Pyramidle/1.0 (Educational Project)',
    'Accept': 'application/json'
}

# Age group indicators
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
    '80+': ('SP.POP.80UP.MA', 'SP.POP.80UP.FE'),
}

def fetch_indicator_data(country_code: str, indicator: str, year_range: str = "2015:2024") -> Optional[float]:
    """Fetch a single indicator value for a country."""
    url = f"{WB_API_BASE}/country/{country_code}/indicator/{indicator}?format=json&date={year_range}&per_page=20"

    try:
        response = requests.get(url, headers=HEADERS, timeout=10)
        response.raise_for_status()
        data = response.json()

        if len(data) > 1 and data[1]:
            for record in data[1]:
                if record.get('value') is not None:
                    return float(record['value'])

        time.sleep(0.1)  # Rate limiting

    except Exception as e:
        print(f"    Error fetching {indicator}: {e}")

    return None

def get_year_births_peaked(country_code: str) -> Optional[int]:
    """Calculate year births peaked from CBR and population data."""
    print(f"    Fetching historical births data...")

    cbr_url = f"{WB_API_BASE}/country/{country_code}/indicator/SP.DYN.CBRT.IN?format=json&date=1960:2024&per_page=100"
    pop_url = f"{WB_API_BASE}/country/{country_code}/indicator/SP.POP.TOTL?format=json&date=1960:2024&per_page=100"

    try:
        cbr_response = requests.get(cbr_url, headers=HEADERS, timeout=15)
        pop_response = requests.get(pop_url, headers=HEADERS, timeout=15)

        cbr_response.raise_for_status()
        pop_response.raise_for_status()

        cbr_json = cbr_response.json()
        pop_json = pop_response.json()

        cbr_data = cbr_json[1] if len(cbr_json) > 1 and cbr_json[1] else []
        pop_data = pop_json[1] if len(pop_json) > 1 and pop_json[1] else []

        if not cbr_data or not pop_data:
            return None

        # Create dictionaries
        cbr_by_year = {}
        for d in cbr_data:
            if d.get('value') is not None:
                cbr_by_year[d['date']] = d['value']

        pop_by_year = {}
        for d in pop_data:
            if d.get('value') is not None:
                pop_by_year[d['date']] = d['value']

        # Calculate births for each year
        births_by_year = {}
        for year in cbr_by_year:
            if year in pop_by_year:
                births = (cbr_by_year[year] / 1000.0) * pop_by_year[year]
                births_by_year[year] = births

        if not births_by_year:
            return None

        # Find year with max births
        max_year = max(births_by_year, key=births_by_year.get)
        return int(max_year)

    except Exception as e:
        print(f"    Error calculating births peak: {e}")
        return None

def check_for_issues(data: Dict) -> Tuple[List[str], bool]:
    """
    Check a country JSON for missing data.

    Returns:
        Tuple of (list of missing age groups, whether yearBirthsPeaked needs fixing)
    """
    missing_age_groups = []
    fix_births_peaked = False

    # Check for 0 values in pyramid
    pyramid = data.get('pyramid', {})
    for gender in ['male', 'female']:
        if gender in pyramid:
            for age_group, value in pyramid[gender].items():
                if value == 0:
                    if age_group not in missing_age_groups:
                        missing_age_groups.append(age_group)

    # Check for default yearBirthsPeaked
    if data.get('yearBirthsPeaked') == 2000:
        fix_births_peaked = True

    return (missing_age_groups, fix_births_peaked)

def fix_country_data(json_path: Path) -> bool:
    """Fix missing data in a country JSON file."""
    try:
        # Read existing data
        with open(json_path, 'r') as f:
            data = json.load(f)

        country_code = data['code']
        country_name = data['name']

        # Check for issues
        missing_age_groups, fix_births_peaked = check_for_issues(data)

        if not missing_age_groups and not fix_births_peaked:
            return False  # No issues found

        print(f"\n{country_name} ({country_code}):")

        fixed_something = False

        # Fix missing age groups
        if missing_age_groups:
            print(f"  Missing age groups: {', '.join(missing_age_groups)}")

            for age_group in missing_age_groups:
                if age_group not in WB_AGE_INDICATORS:
                    print(f"    Warning: Unknown age group {age_group}")
                    continue

                male_indicator, female_indicator = WB_AGE_INDICATORS[age_group]

                print(f"    Fetching {age_group}...", end=" ")
                male_value = fetch_indicator_data(country_code, male_indicator)
                female_value = fetch_indicator_data(country_code, female_indicator)

                if male_value is not None and female_value is not None:
                    data['pyramid']['male'][age_group] = int(male_value)
                    data['pyramid']['female'][age_group] = int(female_value)
                    print(f"✓ Fixed (M: {int(male_value):,}, F: {int(female_value):,})")
                    fixed_something = True
                else:
                    print(f"✗ Still unavailable")

        # Fix yearBirthsPeaked
        if fix_births_peaked:
            print(f"  Year births peaked is default (2000), recalculating...")
            year_peaked = get_year_births_peaked(country_code)

            if year_peaked and year_peaked != 2000:
                data['yearBirthsPeaked'] = year_peaked
                print(f"    ✓ Updated to {year_peaked}")
                fixed_something = True
            else:
                print(f"    ✗ Could not determine (keeping 2000)")

        # Save if we fixed anything
        if fixed_something:
            with open(json_path, 'w') as f:
                json.dump(data, f, indent=2)
            return True

        return False

    except Exception as e:
        print(f"  Error processing {json_path}: {e}")
        return False

def main():
    """Main function to fix all country JSON files with issues."""
    print("=" * 60)
    print("Pyramidle: Fix Missing Data")
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

    # First pass: identify files with issues
    print("Scanning for issues...")
    files_with_issues = []

    for json_file in json_files:
        try:
            with open(json_file, 'r') as f:
                data = json.load(f)

            missing_age_groups, fix_births_peaked = check_for_issues(data)

            if missing_age_groups or fix_births_peaked:
                issues = []
                if missing_age_groups:
                    issues.append(f"{len(missing_age_groups)} missing age groups")
                if fix_births_peaked:
                    issues.append("default births peak year")

                files_with_issues.append(json_file)
                print(f"  {data['name']} ({data['code']}): {', '.join(issues)}")

        except Exception as e:
            print(f"  Error reading {json_file}: {e}")

    if not files_with_issues:
        print("\n✓ No issues found! All files are complete.")
        return

    print(f"\nFound {len(files_with_issues)} files with issues")
    print("=" * 60)
    print("Starting fixes...")

    # Fix files
    fixed_count = 0

    for json_file in files_with_issues:
        if fix_country_data(json_file):
            fixed_count += 1

    print()
    print("=" * 60)
    print(f"Fixed: {fixed_count} countries")
    print(f"Could not fix: {len(files_with_issues) - fixed_count} countries")
    print("=" * 60)

if __name__ == '__main__':
    main()
