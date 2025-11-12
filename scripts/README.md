# Data Download Scripts

This directory contains scripts to download real demographic data for all countries.

## Download Demographic Data

The `download_demographic_data.py` script fetches data from the UN World Population Prospects 2022 database.

### Data Sources

- **UN World Population Prospects 2022**: Age/sex population pyramids, fertility rates, life expectancy, median age, births data
- All data is for the year 2022 (most recent complete dataset)

### Requirements

Python 3.7+ with the following packages:

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
1. Fetch list of all countries from UN API
2. For each country, download:
   - Population pyramid (age/sex distribution)
   - Total Fertility Rate (TFR)
   - Median Age
   - Life Expectancy
   - Crude Birth Rate
   - Historical births data to find year births peaked
3. Save data to `public/data/countries/` as JSON files
4. Generate `public/data/countries.json` with list of all countries

### Output Format

Each country file (`public/data/countries/{CODE}.json`) contains:

```json
{
  "code": "USA",
  "name": "United States of America",
  "population": 331900000,
  "totalFertilityRate": 1.66,
  "medianAge": 38.5,
  "yearBirthsPeaked": 2007,
  "lifeExpectancy": 77.2,
  "crudeBirthRate": 11.0,
  "pyramid": {
    "male": {
      "0-4": 9820000,
      "5-9": 10230000,
      ...
    },
    "female": {
      "0-4": 9390000,
      "5-9": 9780000,
      ...
    }
  }
}
```

### Notes

- The script includes rate limiting (0.5s delay between countries) to be respectful to the UN API
- Countries without complete data will use reasonable defaults
- Download takes approximately 5-10 minutes for all ~200 countries
- No API key required - the UN Data Portal API is free and open

### Troubleshooting

**Error: "No module named 'requests'"**
```bash
pip install requests pandas
```

**Error: Connection timeout**
- Check internet connection
- The UN API may be temporarily unavailable, try again later
- Consider increasing delays in the script if rate limited

**Missing data for some countries**
- Some small territories may not have complete demographic data in the UN database
- The script will use reasonable defaults for missing indicators
- Check console output for warnings about missing data
