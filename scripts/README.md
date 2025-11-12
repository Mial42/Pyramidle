# Data Download Scripts

This directory contains scripts to download real demographic data for all countries.

## Download Demographic Data

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
- **80+ age group**: World Bank only has "80+" category, which is split 60/40 into "80-84" and "85+" age groups
- **Median age**: Calculated from population pyramid using weighted average of age group midpoints

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
