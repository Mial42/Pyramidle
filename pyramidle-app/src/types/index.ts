// Age groups for population pyramid
export type AgeGroup =
  | '0-4' | '5-9' | '10-14' | '15-19' | '20-24' | '25-29'
  | '30-34' | '35-39' | '40-44' | '45-49' | '50-54' | '55-59'
  | '60-64' | '65-69' | '70-74' | '75-79' | '80+';

// Population data by age group and gender
export interface PyramidData {
  male: Record<AgeGroup, number>;
  female: Record<AgeGroup, number>;
}

// Complete country data including demographics
export interface CountryData {
  code: string;
  name: string;
  population: number;
  totalFertilityRate: number;
  medianAge: number;
  yearBirthsPeaked: number;
  lifeExpectancy: number;
  crudeBirthRate: number;
  pyramid: PyramidData;
}

// Hint types for progressive reveal
export interface Hint {
  type: 'tfr' | 'medianAge' | 'birthsPeak' | 'lifeExpectancy' | 'cbr';
  label: string;
  value: string;
}

// Game state
export interface GameState {
  targetCountry: CountryData;
  guesses: string[]; // Country codes
  hintsRevealed: Hint[];
  gameStatus: 'playing' | 'won' | 'lost';
  currentGuess: number; // 0-4
}

// Statistics tracking
export interface Statistics {
  gamesPlayed: number;
  gamesWon: number;
  currentStreak: number;
  maxStreak: number;
  guessDistribution: number[]; // Index 0 = won on guess 1, etc.
}
