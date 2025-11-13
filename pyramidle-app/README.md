# Pyramidle

A Wordle-style game for guessing countries from their population pyramids.

## Development

### Running the App

There are two development modes available:

#### User Mode (Production View)
```bash
npm run dev
# or
npm run dev:user
```
- Runs on **http://localhost:5173**
- Shows the production view (no test controls)
- Same experience as end users will see

#### Test Mode (Developer View)
```bash
npm run dev:test
```
- Runs on **http://localhost:5174**
- Shows test mode controls for cycling through countries
- Yellow banner at top indicates test mode
- Use this for testing and development

### Running Both Modes Simultaneously

You can run both modes at the same time in separate terminals:

```bash
# Terminal 1 - User view
npm run dev:user

# Terminal 2 - Test view
npm run dev:test
```

Then visit:
- User mode: http://localhost:5173
- Test mode: http://localhost:5174

### Environment Variables

The app uses Vite environment variables:

- `.env` - Default environment (user mode)
- `.env.test` - Test mode environment
- `.env.local` - Local overrides (gitignored)

Current variables:
- `VITE_TEST_MODE` - Set to `true` to enable test controls

## Building

```bash
npm run build
```

Builds the production version to the `dist/` directory.

## Project Structure

```
pyramidle-app/
├── public/
│   └── data/
│       ├── countries.json       # List of all countries
│       └── countries/           # Individual country data files
│           ├── USA.json
│           ├── CHN.json
│           └── ...
├── src/
│   ├── components/              # React components
│   ├── hooks/                   # Custom React hooks
│   ├── types/                   # TypeScript type definitions
│   ├── utils/                   # Utility functions
│   │   ├── dailyCountry.ts     # Daily country selection logic
│   │   └── hintGenerator.ts    # Progressive hint system
│   └── App.tsx                  # Main application component
├── .env                         # User mode environment
├── .env.test                    # Test mode environment
└── package.json
```

## Game Mechanics

- **Daily Challenge**: Everyone gets the same country each day (changes at UTC midnight)
- **Country Selection**: Weighted by log(min(population, 100M)) to balance variety
- **6 Guesses**: Players have 6 attempts to guess the correct country
- **Progressive Hints**: After each incorrect guess, a new hint is revealed:
  1. Total Fertility Rate (TFR)
  2. Median Age
  3. Year Births Peaked
  4. Life Expectancy
  5. Crude Birth Rate (CBR)

## Data Sources

- Population pyramids: World Bank Open Data API
- Demographic indicators: World Bank
- Births data: UN World Population Prospects 2024 (via Our World in Data)

Data year: 2023 for most countries
