# Data Download Scripts

This directory contains scripts to download and process demographic data for all countries.

## Scripts Overview

1. **`download_demographic_data.py`**: Downloads complete demographic data from World Bank API
2. **`update_year_births_peaked.py`**: Updates year births peaked using actual births data

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
