#!/usr/bin/env python3
"""
Generate demographic rankings for all countries.
This should be run after downloading/updating country data.
Rankings are saved as a JSON file and loaded by the app.
"""

import json
from pathlib import Path
from typing import List, Dict, Any

def get_years_before_peak(country: Dict[str, Any]) -> float:
    """Convert yearBirthsPeaked to years before dataYear"""
    data_year = country.get('dataYear', 2023)
    year_peaked = country.get('yearBirthsPeaked')

    if isinstance(year_peaked, str):
        # "Has not peaked yet" = 0
        return 0

    return data_year - year_peaked

def load_all_countries(countries_dir: Path) -> List[Dict[str, Any]]:
    """Load all country JSON files"""
    countries = []

    for json_file in countries_dir.glob('*.json'):
        with open(json_file, 'r', encoding='utf-8') as f:
            country = json.load(f)
            countries.append(country)

    return countries

def create_rankings(countries: List[Dict[str, Any]]) -> Dict[str, List[Dict[str, Any]]]:
    """
    Create ranked lists for each demographic metric.
    Returns a dict with lists of {code, value} sorted by value.
    """

    # Population ranking
    population = [
        {'code': c['code'], 'value': c['population']}
        for c in countries
    ]
    population.sort(key=lambda x: x['value'])

    # TFR ranking
    tfr = [
        {'code': c['code'], 'value': c['totalFertilityRate']}
        for c in countries
    ]
    tfr.sort(key=lambda x: x['value'])

    # Median age ranking
    median_age = [
        {'code': c['code'], 'value': c['medianAge']}
        for c in countries
    ]
    median_age.sort(key=lambda x: x['value'])

    # Years before peak ranking
    years_before_peak = [
        {'code': c['code'], 'value': get_years_before_peak(c)}
        for c in countries
    ]
    years_before_peak.sort(key=lambda x: x['value'])

    # Life expectancy ranking
    life_expectancy = [
        {'code': c['code'], 'value': c['lifeExpectancy']}
        for c in countries
    ]
    life_expectancy.sort(key=lambda x: x['value'])

    # CBR ranking
    cbr = [
        {'code': c['code'], 'value': c['crudeBirthRate']}
        for c in countries
    ]
    cbr.sort(key=lambda x: x['value'])

    return {
        'population': population,
        'tfr': tfr,
        'medianAge': median_age,
        'yearsBeforePeak': years_before_peak,
        'lifeExpectancy': life_expectancy,
        'cbr': cbr,
    }

def main():
    # Path to countries directory
    countries_dir = Path(__file__).parent.parent / 'pyramidle-app' / 'public' / 'data' / 'countries'

    if not countries_dir.exists():
        print(f"Error: Countries directory not found: {countries_dir}")
        return 1

    print(f"Loading countries from {countries_dir}...")
    countries = load_all_countries(countries_dir)
    print(f"Loaded {len(countries)} countries")

    print("Calculating rankings...")
    rankings = create_rankings(countries)

    # Save rankings to JSON
    output_path = countries_dir.parent / 'rankings.json'
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(rankings, f, indent=2)

    print(f"✓ Rankings saved to {output_path}")
    print(f"  Population: {len(rankings['population'])} countries")
    print(f"  TFR: {len(rankings['tfr'])} countries")
    print(f"  Median Age: {len(rankings['medianAge'])} countries")
    print(f"  Years Before Peak: {len(rankings['yearsBeforePeak'])} countries")
    print(f"  Life Expectancy: {len(rankings['lifeExpectancy'])} countries")
    print(f"  CBR: {len(rankings['cbr'])} countries")

    return 0

if __name__ == '__main__':
    exit(main())
