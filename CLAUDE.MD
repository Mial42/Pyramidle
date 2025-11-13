# Instructions for Claude

## Critical Data Integrity Rules

### NEVER Fake or Impute Data

**YOU MUST NEVER:**
- Generate fake data values
- Impute missing data values
- Fill in placeholder data
- Estimate or guess at data values
- Create synthetic data without explicit authorization

**If data is missing or unavailable:**
- Report the missing data to the user
- Ask the user how they want to handle it
- Use scripts or APIs to fetch real data if available
- Document any data gaps clearly

### NEVER Directly Modify .json Files

**YOU MUST NEVER:**
- Directly edit .json files using the Edit or Write tools
- Manually change values in JSON data files
- Update JSON files without using proper data processing scripts

**Instead, you should:**
- Use or create Python scripts to modify JSON files programmatically
- Leverage existing data processing utilities in the codebase
- Fetch data from authoritative sources (APIs, databases)
- Let the user review any data modification scripts before running them

## Why These Rules Exist

1. **Data Integrity**: Manual edits and imputed data compromise the reliability of the dataset
2. **Reproducibility**: Script-based modifications are repeatable and auditable
3. **Accuracy**: Real data from authoritative sources ensures correctness
4. **Transparency**: Users must know when data is missing rather than having fake data silently inserted

## When in Doubt

Always ask the user for guidance rather than making assumptions about data values or file modifications.
