# Data Download Scripts

This directory contains scripts to download and process demographic data for all countries.

## Scripts Overview

1. **`download_demographic_data.py`**: Downloads complete demographic data from World Bank API
2. **`update_year_births_peaked.py`**: Updates year births peaked using actual births data
3. **`fix_missing_data.py`**: Fixes country JSONs with missing or default values
4. **`add_data_year.py`**: Adds dataYear field to existing country JSONs
5. **`generate_rankings.py`**: Generates pre-calculated demographic rankings for all countries

## 1. Download Demographic Data

The `download_demographic_data.py` script fetches data from the World Bank Open Data API.

### Data Source

- **World Bank Open Data API**: Age/sex population pyramids, fertility rates, life expectancy, crude birth rate
- Data is from the most recent available year (typically 2022-2023)
- Falls back to earlier years if current data not available

### Requirements

Python 3.7+ with requests:

```bash
pip install -r requirements.txt
```

### Usage

Run from the Pyramidle root directory:

```bash
cd Pyramidle
python scripts/download_demographic_data.py
```

The script will:
1. Fetch list of all countries from World Bank API
2. For each country, download:
   - Population pyramid (18 age groups by sex)
   - Total Fertility Rate (TFR)
   - Life Expectancy
   - Crude Birth Rate
   - Median Age (calculated from pyramid)
   - Year births peaked (calculated from historical data)
3. Save data to `public/data/countries/` as JSON files
4. Generate `public/data/countries.json` with list of all countries

### Output Format

Each country file (`public/data/countries/{CODE}.json`) contains:

```json
{
  "code": "USA",
  "name": "United States",
  "population": 331900000,
  "totalFertilityRate": 1.66,
  "medianAge": 38.5,
  "yearBirthsPeaked": 2007,
  "lifeExpectancy": 77.2,
  "crudeBirthRate": 11.0,
  "pyramid": {
    "male": {
      "0-4": 9820000,
      ...
    },
    "female": {
      "0-4": 9390000,
      ...
    }
  }
}
```

### Notes

- The script includes rate limiting (0.3s delay between countries) to be respectful to the World Bank API
- Countries without sufficient data will be skipped
- Download takes approximately 5-10 minutes for all ~200 countries
- No API key required - World Bank Open Data API is free
- **80+ age group**: World Bank only has "80+" as a single category
- **Median age**: Calculated from population pyramid using weighted average of age group midpoints
- **Year births peaked**: May not be accurate for all countries; use `update_year_births_peaked.py` to fix

### Troubleshooting

**Error: "No module named 'requests'"**
```bash
pip install requests
```

**Error: Connection timeout**
- Check internet connection
- The World Bank API may be temporarily unavailable, try again later

**Missing data for some countries**
- Some small territories may not have complete demographic data
- The script will skip countries with insufficient age/sex data
- Check console output for warnings about missing data

## 2. Update Year Births Peaked

The `update_year_births_peaked.py` script fixes the `yearBirthsPeaked` field using actual historical births data.

### Why Use This Script?

The main download script tries to calculate year births peaked from crude birth rate × population, but this often fails or defaults to 2000. This script uses actual births data from reliable sources to get the correct year.

### Data Sources

Tries these sources in order:
1. **Our World in Data** (UN World Population Prospects 2024)
2. **UN World Population Prospects** direct download
3. **Local CSV file** if provided with `--file` option

### Requirements

```bash
pip install requests pandas
```

### Usage

**Option 1: Auto-download** (if APIs are accessible):
```bash
python scripts/update_year_births_peaked.py
```

**Option 2: Use local CSV file**:
```bash
python scripts/update_year_births_peaked.py --file births_data.csv
```

### Manual Download Instructions

If auto-download fails (blocked APIs, network issues):

1. Visit: https://ourworldindata.org/grapher/births-and-deaths-projected-to-2100
2. Click "Download" → "Full data (CSV)"
3. Save the file (e.g., `births_data.csv`)
4. Run: `python scripts/update_year_births_peaked.py --file births_data.csv`

**Alternative UN source:**
- UN WPP 2024: https://population.un.org/wpp/Download/Standard/CSV/
- Download "WPP2024_Demographic_Indicators_Medium.csv"

### What It Does

1. Downloads or loads births data (historical births by country and year)
2. For each country JSON file in `public/data/countries/`:
   - Finds the year with maximum births
   - Updates the `yearBirthsPeaked` field
   - Preserves all other fields unchanged
3. Prints summary of updated vs not found countries

### Example Output

```
Processing United States (USA)...
  United States: Births peaked in 2007 with 4,316,234 births
  Updated USA.json: 2000 -> 2007

Processing Afghanistan (AFG)...
  Afghanistan: Births peaked in 2018 with 1,254,389 births
  Updated AFG.json: 2000 -> 2018
```

### Country Name Mapping

The script handles country name differences between data sources. Edit `COUNTRY_NAME_OVERRIDES` in the script if you need to add mappings:

```python
COUNTRY_NAME_OVERRIDES = {
    'USA': 'United States',
    'GBR': 'United Kingdom',
    'RUS': 'Russia',
    # Add more as needed
}
```

### Workflow Recommendation

```bash
# 1. Download all demographic data first
python scripts/download_demographic_data.py

# 2. Fix year births peaked for all countries
python scripts/update_year_births_peaked.py

# Or if auto-download doesn't work:
# 2a. Download CSV manually from Our World in Data
# 2b. Run with local file
python scripts/update_year_births_peaked.py --file births_data.csv
```

## 3. Fix Missing Data

The `fix_missing_data.py` script fixes country JSON files that have missing or default values.

### What It Fixes

1. **Age pyramid values of 0**: Sometimes the API fails to return data for specific age groups, resulting in 0 values
2. **yearBirthsPeaked = 2000**: When the births peak calculation fails, it defaults to 2000
3. **totalFertilityRate = 2.1**: Default value when TFR data is unavailable
4. **lifeExpectancy = 70.0**: Default value when life expectancy data is unavailable
5. **crudeBirthRate = 20.0**: Default value when CBR data is unavailable

### Why This Happens

- Network timeouts during initial download
- Temporary API unavailability for specific indicators
- Rate limiting causing some requests to fail
- Missing data for certain country/indicator combinations

### Usage

```bash
python scripts/fix_missing_data.py
```

### What It Does

1. **Scans all country JSON files** for issues:
   - Checks each age group in the pyramid for 0 values
   - Checks if yearBirthsPeaked is 2000 (the default fallback)

2. **Reports all issues found**:
   ```
   Found 12 files with issues
     France (FRA): 1 missing age groups
     Afghanistan (AFG): default births peak year, default life expectancy
     Somalia (SOM): 3 missing age groups, default births peak year, default TFR
   ```

3. **Fixes each issue**:
   - Re-fetches only the missing age group data from World Bank API
   - Re-fetches TFR, life expectancy, and CBR if they have default values
   - Re-calculates yearBirthsPeaked if it's 2000
   - Updates the JSON file with corrected values
   - Preserves all other data unchanged

### Example Output

```
France (FRA):
  Missing age groups: 70-74
    Fetching 70-74... ✓ Fixed (M: 1,545,892, F: 1,789,234)

Afghanistan (AFG):
  Life expectancy is default (70.0), refetching...
    ✓ Updated to 63.2
  Year births peaked is default (2000), recalculating...
    Fetching historical births data...
    ✓ Updated to 2018

Somalia (SOM):
  Total fertility rate is default (2.1), refetching...
    ✓ Updated to 6.12
  Crude birth rate is default (20.0), refetching...
    ✓ Updated to 42.5
```

### When to Use

Run this script after:
- Initial data download completes
- You notice countries with 0 values in pyramids
- Many countries showing yearBirthsPeaked = 2000

### Performance

- Much faster than re-downloading everything
- Only makes API calls for missing data
- Typical runtime: 1-3 minutes for fixing 10-20 countries

## 4. Add Data Year

The `add_data_year.py` script adds the `dataYear` field to existing country JSON files.

### Usage

```bash
python scripts/add_data_year.py
```

### What It Does

- Queries World Bank API to find the actual year of demographic data for each country
- Adds `dataYear` field to JSON files that don't have it
- Makes only 1 API call per country (checks population total indicator)

### When to Use

- After downloading data with older version of script
- If you have country JSONs without `dataYear` field

## 5. Generate Rankings

The `generate_rankings.py` script creates pre-calculated demographic rankings for all countries.

### Purpose

The app uses rank-based distance calculation to determine how close a guess is to the target country on each metric. Instead of calculating these rankings in the browser (expensive), we pre-calculate them once and save as a static JSON file.

**IMPORTANT**: This script must be run after any changes to country data files (after running download, update, or fix scripts).

### Usage

```bash
python scripts/generate_rankings.py
```

The script will:
1. Load all country JSON files from `pyramidle-app/public/data/countries/`
2. Sort countries by each metric (population, TFR, median age, etc.)
3. Save rankings to `pyramidle-app/public/data/rankings.json`

### Output

Creates `pyramidle-app/public/data/rankings.json` with sorted lists:

```json
{
  "population": [
    {"code": "VAT", "value": 825},
    {"code": "NRU", "value": 12668},
    ...
  ],
  "tfr": [...],
  "medianAge": [...],
  "yearsBeforePeak": [...],
  "lifeExpectancy": [...],
  "cbr": [...]
}
```

Each list is sorted by value (lowest to highest), and the app uses these to calculate rank distances.

### When to Run

Run this script:
- After downloading new country data
- After updating any country data files
- After fixing missing data
- Whenever country JSONs change

The rankings are loaded by the React app and used for all distance calculations in the share results feature.

## Complete Workflow

```bash
# Step 1: Download all demographic data
python scripts/download_demographic_data.py

# Step 2: Fix any missing/default values
python scripts/fix_missing_data.py

# Step 3: Update year births peaked with actual births data
python scripts/update_year_births_peaked.py --file births_data.csv

# Step 4 (optional): Add dataYear if missing
python scripts/add_data_year.py

# Step 5: REQUIRED - Generate rankings for the app
python scripts/generate_rankings.py
```
