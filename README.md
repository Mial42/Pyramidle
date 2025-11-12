# Pyramidle

A daily geography game where you guess the country based on its population pyramid. Inspired by [Tradle](https://oec.world/en/games/tradle), but using demographic data instead of export profiles.

## Game Concept

**Objective**: Guess the mystery country in 5 tries or fewer by analyzing its population pyramid.

**How to Play**:
1. You're shown a population pyramid (age-sex distribution) and total population
2. Make a guess by selecting a country from the dropdown
3. After each incorrect guess, receive a hint about the mystery country
4. Win by guessing correctly within 5 attempts
5. A new country is featured each day

## Features

### Core Gameplay
- **Population Pyramid Visualization**: Interactive chart showing age and gender distribution
- **5 Guesses Maximum**: Limited attempts add challenge
- **Progressive Hints**: Get more information after each wrong guess
- **Daily Puzzle**: One country per day (midnight UTC reset)
- **Test Mode**: Cycle through countries quickly for development/testing

### User Experience
- **Guess History**: Track your guesses and hints received
- **Statistics Dashboard**: Win streak, total games played, win percentage
- **Share Results**: Copy emoji/text summary to share on social media (like Wordle)
- **Responsive Design**: Works on desktop and mobile
- **Dark Mode**: Optional dark theme

### Data Features
- **Comprehensive Country Database**: ~195 countries with demographic data
- **Real Demographic Data**: Using UN/World Bank population statistics
- **Smart Hint System**: Geographic, economic, and demographic clues

## Hint System

After each incorrect guess, reveal one hint (in order):

1. **Total Fertility Rate (TFR)**: Average number of children per woman (e.g., "TFR: 1.5-2.0", "TFR: 4.5-5.0")
2. **Median Age**: Approximate value (e.g., "Median age: 35-40 years")
3. **Year Births Peaked**: The year in which the country had the most births (e.g., "Births peaked: 1985-1990")
4. **Life Expectancy**: Average lifespan (e.g., "Life expectancy: 78-82 years")
5. **Crude Birth Rate**: Births per 1,000 people per year (e.g., "CBR: 10-15 per 1,000")

## Tech Stack (Proposed)

### Frontend
- **Framework**: React with TypeScript
- **Charting**: D3.js or Chart.js for population pyramids
- **Styling**: Tailwind CSS
- **State Management**: React Context or Zustand
- **Country Search**: react-select or custom autocomplete

### Data & Logic
- **Data Source**: Static JSON files with preprocessed demographic data
  - Sources: UN Population Division, World Bank Open Data
- **Daily Country Selection**: Seeded random based on date (deterministic)
- **Storage**: LocalStorage for user statistics and game state

### Deployment
- **Hosting**: Vercel, Netlify, or GitHub Pages (static site)
- **Domain**: Custom domain (optional)

## Project Structure

```
pyramidle/
├── public/
│   ├── data/
│   │   ├── countries.json          # Country list with metadata
│   │   └── pyramids/
│   │       ├── AFG.json            # Afghanistan population data
│   │       ├── USA.json            # United States population data
│   │       └── ...                 # One file per country (ISO code)
│   └── index.html
├── src/
│   ├── components/
│   │   ├── PopulationPyramid.tsx   # Chart component
│   │   ├── CountryInput.tsx        # Search/select country
│   │   ├── GuessHistory.tsx        # List of guesses and hints
│   │   ├── HintDisplay.tsx         # Show current hints
│   │   ├── Statistics.tsx          # User stats modal
│   │   ├── ShareButton.tsx         # Share results
│   │   └── TestModeControls.tsx    # Dev controls for cycling countries
│   ├── hooks/
│   │   ├── useGameState.ts         # Game logic and state
│   │   ├── useStatistics.ts        # Track user performance
│   │   └── useDailyCountry.ts      # Daily country selection
│   ├── utils/
│   │   ├── dateUtils.ts            # Date handling for daily puzzles
│   │   ├── hintGenerator.ts        # Generate hints based on country data
│   │   └── shareUtils.ts           # Format share text
│   ├── types/
│   │   └── index.ts                # TypeScript types
│   ├── App.tsx
│   └── main.tsx
├── scripts/
│   └── processData.js              # Convert raw demographic data to JSON
├── package.json
├── tsconfig.json
└── README.md
```

## Data Requirements

### Country Data Structure

```json
{
  "code": "USA",
  "name": "United States",
  "population": 331900000,
  "totalFertilityRate": 1.78,
  "medianAge": 38.5,
  "yearBirthsPeaked": 1990,
  "lifeExpectancy": 78.9,
  "crudeBirthRate": 11.0,
  "pyramid": {
    "male": {
      "0-4": 9820000,
      "5-9": 10230000,
      "10-14": 10580000,
      "15-19": 10800000,
      "20-24": 11250000,
      "25-29": 11870000,
      "30-34": 11420000,
      "35-39": 10650000,
      "40-44": 10180000,
      "45-49": 10120000,
      "50-54": 10630000,
      "55-59": 11100000,
      "60-64": 10340000,
      "65-69": 8920000,
      "70-74": 7230000,
      "75-79": 5340000,
      "80-84": 3560000,
      "85+": 2450000
    },
    "female": {
      "0-4": 9390000,
      "5-9": 9780000,
      "10-14": 10110000,
      "15-19": 10320000,
      "20-24": 10760000,
      "25-29": 11380000,
      "30-34": 10980000,
      "35-39": 10320000,
      "40-44": 9930000,
      "45-49": 9960000,
      "50-54": 10590000,
      "55-59": 11200000,
      "60-64": 10640000,
      "65-69": 9570000,
      "70-74": 8050000,
      "75-79": 6320000,
      "80-84": 4550000,
      "85+": 4120000
    }
  }
}
```

### Data Sources
- **UN Population Division**: World Population Prospects
- **World Bank**: Population indicators, income classifications
- Age groups: Standard 5-year intervals (0-4, 5-9, ..., 80-84, 85+)

## Implementation Plan

### Phase 1: Setup & Data Preparation
- [ ] Initialize React + TypeScript project
- [ ] Set up development environment
- [ ] Download and process demographic data
- [ ] Create country database JSON files
- [ ] Define TypeScript interfaces

### Phase 2: Core Visualization
- [ ] Build population pyramid component
- [ ] Implement responsive chart scaling
- [ ] Add male/female color coding
- [ ] Display total population

### Phase 3: Game Logic
- [ ] Implement daily country selection (seeded random)
- [ ] Create country search/input component
- [ ] Build guess validation
- [ ] Implement 5-guess limit
- [ ] Add win/loss detection

### Phase 4: Hint System
- [ ] Develop hint generation logic
- [ ] Create hint display component
- [ ] Implement progressive hint reveal
- [ ] Test hint accuracy

### Phase 5: User Features
- [ ] LocalStorage for game state persistence
- [ ] Statistics tracking (wins, streak, etc.)
- [ ] Share functionality with emoji grid
- [ ] Statistics modal/dashboard

### Phase 6: Polish & Testing
- [ ] Responsive design (mobile + desktop)
- [ ] Dark mode implementation
- [ ] Test mode for development
- [ ] Cross-browser testing
- [ ] Accessibility improvements

### Phase 7: Deployment
- [ ] Build optimization
- [ ] Deploy to hosting platform
- [ ] Set up custom domain (optional)
- [ ] Analytics (optional)

## Testing Strategy

### Test Mode Features
- **Manual Country Selection**: Choose specific countries to test
- **Skip Timer**: Don't wait 24 hours for next puzzle
- **Reset Statistics**: Clear localStorage for fresh testing
- **Hint Preview**: See all hints at once for verification

### Test Cases
- Countries with unusual pyramids (aging populations, youth bulges)
- Edge cases (small islands, city-states)
- Verify hint accuracy across all countries
- Test date transition logic
- Validate share text formatting

## Future Enhancements (Post-MVP)

- **Hard Mode**: No hints, or more restricted hints
- **Archive Mode**: Play previous days' puzzles
- **Leaderboards**: Optional global statistics
- **Multiplayer**: Challenge friends to same puzzle
- **Educational Mode**: Learn about demographics after solving
- **Historical Data**: Compare current vs. past population pyramids
- **Subnational Data**: States, provinces for select countries

## Success Metrics

- **Engagement**: Daily active users, return rate
- **Difficulty**: Average guesses to win, win percentage
- **Virality**: Share rate, social media mentions
- **Data Quality**: User feedback on hint accuracy

---

## Getting Started (For Developers)

*Installation and development instructions will be added once implementation begins.*

## Contributing

*Contribution guidelines will be added once the project is public.*

## License

*License to be determined.*

## Acknowledgments

- Inspired by [Tradle](https://oec.world/en/games/tradle)
- Demographic data from UN Population Division and World Bank
- Built with React, TypeScript, and D3.js

---

**Status**: Planning phase - implementation not yet started
