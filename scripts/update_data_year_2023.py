#!/usr/bin/env python3
"""
Update dataYear to 2023 for all countries and set yearBirthsPeaked to
"Has not peaked yet" for countries where births peaked in 2023.

This handles countries with rapidly growing populations where births are
still increasing as of the most recent data year.

Requirements:
    None (uses only standard library)
"""

import json
from pathlib import Path
from typing import Dict

def update_country_file(json_path: Path) -> bool:
    """
    Update dataYear and yearBirthsPeaked in a country JSON file.

    Returns:
        True if file was updated, False otherwise
    """
    try:
        # Read existing data
        with open(json_path, 'r') as f:
            data = json.load(f)

        country_code = data['code']
        country_name = data['name']

        changed = False
        changes = []

        # Update dataYear to 2023
        old_data_year = data.get('dataYear')
        if old_data_year != 2023:
            data['dataYear'] = 2023
            changes.append(f"dataYear: {old_data_year} → 2023")
            changed = True

        # Update yearBirthsPeaked if it's 2023
        old_year_peaked = data.get('yearBirthsPeaked')
        if old_year_peaked == 2023:
            data['yearBirthsPeaked'] = "Has not peaked yet"
            changes.append(f"yearBirthsPeaked: 2023 → 'Has not peaked yet'")
            changed = True

        # Save if we made changes
        if changed:
            with open(json_path, 'w') as f:
                json.dump(data, f, indent=2)

            print(f"{country_name} ({country_code}): {', '.join(changes)}")
            return True

        return False

    except Exception as e:
        print(f"Error processing {json_path}: {e}")
        return False

def main():
    """Main function to update all country JSON files."""
    print("=" * 60)
    print("Pyramidle: Update Data Year to 2023")
    print("=" * 60)
    print()

    # Find country JSON files
    countries_dir = Path(__file__).parent.parent / 'pyramidle-app' / 'public' / 'data' / 'countries'

    if not countries_dir.exists():
        print(f"Error: Countries directory not found at {countries_dir}")
        return

    json_files = sorted(list(countries_dir.glob('*.json')))
    print(f"Found {len(json_files)} country JSON files")
    print()

    # Process each country
    updated_count = 0
    not_peaked_count = 0

    for json_file in json_files:
        try:
            with open(json_file, 'r') as f:
                data = json.load(f)

            # Track if this country's births haven't peaked yet
            if data.get('yearBirthsPeaked') == 2023:
                not_peaked_count += 1

            if update_country_file(json_file):
                updated_count += 1

        except Exception as e:
            print(f"Error reading {json_file}: {e}")

    print()
    print("=" * 60)
    print(f"Updated: {updated_count} countries")
    print(f"Countries where births have not peaked yet: {not_peaked_count}")
    print("=" * 60)

if __name__ == '__main__':
    main()
