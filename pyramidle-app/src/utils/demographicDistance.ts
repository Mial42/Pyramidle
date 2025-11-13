import type { CountryData } from '../types';

/**
 * Convert yearBirthsPeaked to years before dataYear
 */
const getYearsBeforePeak = (country: CountryData): number => {
  const dataYear = country.dataYear || 2023;
  if (typeof country.yearBirthsPeaked === 'string') {
    // "Has not peaked yet" = 0
    return 0;
  }
  return dataYear - country.yearBirthsPeaked;
};

/**
 * Country with its value for a specific metric
 */
interface RankedCountry {
  code: string;
  value: number;
}

/**
 * Rankings for all demographic metrics
 */
export interface DemographicRankings {
  population: RankedCountry[];
  tfr: RankedCountry[];
  medianAge: RankedCountry[];
  yearsBeforePeak: RankedCountry[];
  lifeExpectancy: RankedCountry[];
  cbr: RankedCountry[];
}

/**
 * Calculate rankings for each demographic dimension
 * Countries are sorted by each metric value
 */
export const calculateDemographicRankings = (countries: CountryData[]): DemographicRankings => {
  if (countries.length === 0) {
    return {
      population: [],
      tfr: [],
      medianAge: [],
      yearsBeforePeak: [],
      lifeExpectancy: [],
      cbr: [],
    };
  }

  // Create ranked lists for each metric
  const population = countries
    .map(c => ({ code: c.code, value: c.population }))
    .sort((a, b) => a.value - b.value);

  const tfr = countries
    .map(c => ({ code: c.code, value: c.totalFertilityRate }))
    .sort((a, b) => a.value - b.value);

  const medianAge = countries
    .map(c => ({ code: c.code, value: c.medianAge }))
    .sort((a, b) => a.value - b.value);

  const yearsBeforePeak = countries
    .map(c => ({ code: c.code, value: getYearsBeforePeak(c) }))
    .sort((a, b) => a.value - b.value);

  const lifeExpectancy = countries
    .map(c => ({ code: c.code, value: c.lifeExpectancy }))
    .sort((a, b) => a.value - b.value);

  const cbr = countries
    .map(c => ({ code: c.code, value: c.crudeBirthRate }))
    .sort((a, b) => a.value - b.value);

  return {
    population,
    tfr,
    medianAge,
    yearsBeforePeak,
    lifeExpectancy,
    cbr,
  };
};

/**
 * Find the rank (position) of a country in a ranked list
 * Returns -1 if not found
 */
const findRank = (rankedList: RankedCountry[], countryCode: string): number => {
  return rankedList.findIndex(item => item.code === countryCode);
};

/**
 * Calculate rank distance between two countries on a single dimension
 * Returns the absolute difference in their positions in the ranking
 */
const calculateRankDistance = (
  rankedList: RankedCountry[],
  guessCode: string,
  targetCode: string
): number => {
  const guessRank = findRank(rankedList, guessCode);
  const targetRank = findRank(rankedList, targetCode);

  if (guessRank === -1 || targetRank === -1) {
    return 999; // Large number if country not found
  }

  return Math.abs(guessRank - targetRank);
};

/**
 * Get color for a rank distance
 * Green (🟩) = within 10 countries
 * Yellow (🟨) = within 30 countries
 * White (⬜) = within 60 countries
 * Red (🟥) = beyond 60 countries
 */
const getColorForRankDistance = (rankDistance: number): string => {
  if (rankDistance <= 10) return '🟩';
  if (rankDistance <= 30) return '🟨';
  if (rankDistance <= 60) return '⬜';
  return '🟥';
};

/**
 * Calculate demographic distances for a guess and return colored squares
 * Returns 6 squares representing: population, TFR, median age, years before peak, life expectancy, CBR
 */
export const calculateGuessSquares = (
  guess: CountryData,
  target: CountryData,
  rankings: DemographicRankings
): string => {
  const rankDistances = [
    // Population
    calculateRankDistance(rankings.population, guess.code, target.code),
    // TFR
    calculateRankDistance(rankings.tfr, guess.code, target.code),
    // Median age
    calculateRankDistance(rankings.medianAge, guess.code, target.code),
    // Years before peak
    calculateRankDistance(rankings.yearsBeforePeak, guess.code, target.code),
    // Life expectancy
    calculateRankDistance(rankings.lifeExpectancy, guess.code, target.code),
    // CBR
    calculateRankDistance(rankings.cbr, guess.code, target.code),
  ];

  return rankDistances.map(getColorForRankDistance).join('');
};

/**
 * Generate shareable result text for Pyramidle
 */
export const generateShareText = (
  date: string,
  guessCount: number | 'X',
  squares: string[]
): string => {
  const header = `#Pyramidle ${date} ${guessCount}/6`;
  const squareLines = squares.join('\n');
  return `${header}\n${squareLines}`;
};
