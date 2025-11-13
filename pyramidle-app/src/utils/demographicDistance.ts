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
 * Calculate min/max for each demographic dimension across all countries
 */
export const calculateDemographicRanges = (countries: CountryData[]) => {
  if (countries.length === 0) {
    return {
      population: { min: 0, max: 1 },
      tfr: { min: 0, max: 1 },
      medianAge: { min: 0, max: 1 },
      yearsBeforePeak: { min: 0, max: 1 },
      lifeExpectancy: { min: 0, max: 1 },
      cbr: { min: 0, max: 1 },
    };
  }

  const populations = countries.map(c => c.population);
  const tfrs = countries.map(c => c.totalFertilityRate);
  const medianAges = countries.map(c => c.medianAge);
  const yearsBeforePeaks = countries.map(c => getYearsBeforePeak(c));
  const lifeExpectancies = countries.map(c => c.lifeExpectancy);
  const cbrs = countries.map(c => c.crudeBirthRate);

  return {
    population: {
      min: Math.min(...populations),
      max: Math.max(...populations),
    },
    tfr: {
      min: Math.min(...tfrs),
      max: Math.max(...tfrs),
    },
    medianAge: {
      min: Math.min(...medianAges),
      max: Math.max(...medianAges),
    },
    yearsBeforePeak: {
      min: Math.min(...yearsBeforePeaks),
      max: Math.max(...yearsBeforePeaks),
    },
    lifeExpectancy: {
      min: Math.min(...lifeExpectancies),
      max: Math.max(...lifeExpectancies),
    },
    cbr: {
      min: Math.min(...cbrs),
      max: Math.max(...cbrs),
    },
  };
};

type DemographicRanges = ReturnType<typeof calculateDemographicRanges>;

/**
 * Normalize a value to 0-1 range based on min/max
 */
const normalize = (value: number, min: number, max: number): number => {
  if (max === min) return 0;
  return (value - min) / (max - min);
};

/**
 * Calculate normalized distance between two countries on a single dimension
 * Returns a value between 0 (identical) and 1 (maximally different)
 */
const calculateDimensionDistance = (
  value1: number,
  value2: number,
  min: number,
  max: number
): number => {
  const normalized1 = normalize(value1, min, max);
  const normalized2 = normalize(value2, min, max);
  return Math.abs(normalized1 - normalized2);
};

/**
 * Get color for a distance value
 * Green (🟩) = within 10% of range
 * Yellow (🟨) = 10-30% of range
 * White (⬜) = >30% of range
 */
const getColorForDistance = (distance: number): string => {
  if (distance <= 0.1) return '🟩';
  if (distance <= 0.3) return '🟨';
  return '⬜';
};

/**
 * Calculate demographic distances for a guess and return colored squares
 * Returns 6 squares representing: population, TFR, median age, years before peak, life expectancy, CBR
 */
export const calculateGuessSquares = (
  guess: CountryData,
  target: CountryData,
  ranges: DemographicRanges
): string => {
  const distances = [
    // Population
    calculateDimensionDistance(
      guess.population,
      target.population,
      ranges.population.min,
      ranges.population.max
    ),
    // TFR
    calculateDimensionDistance(
      guess.totalFertilityRate,
      target.totalFertilityRate,
      ranges.tfr.min,
      ranges.tfr.max
    ),
    // Median age
    calculateDimensionDistance(
      guess.medianAge,
      target.medianAge,
      ranges.medianAge.min,
      ranges.medianAge.max
    ),
    // Years before peak
    calculateDimensionDistance(
      getYearsBeforePeak(guess),
      getYearsBeforePeak(target),
      ranges.yearsBeforePeak.min,
      ranges.yearsBeforePeak.max
    ),
    // Life expectancy
    calculateDimensionDistance(
      guess.lifeExpectancy,
      target.lifeExpectancy,
      ranges.lifeExpectancy.min,
      ranges.lifeExpectancy.max
    ),
    // CBR
    calculateDimensionDistance(
      guess.crudeBirthRate,
      target.crudeBirthRate,
      ranges.cbr.min,
      ranges.cbr.max
    ),
  ];

  return distances.map(getColorForDistance).join('');
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
