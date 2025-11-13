import type { CountryData, Hint } from '../types';

// Format TFR hint - show exact value
const formatTFR = (tfr: number): string => {
  return tfr.toFixed(2);
};

// Format median age hint - show exact value
const formatMedianAge = (age: number): string => {
  return `${age.toFixed(1)} years`;
};

// Format births peak year hint - show exact value or "Has not peaked yet"
const formatBirthsPeak = (year: number | string): string => {
  if (typeof year === 'string') {
    return year; // Return as-is if it's already a string (e.g., "Has not peaked yet")
  }
  return year.toString();
};

// Format life expectancy hint - show exact value
const formatLifeExpectancy = (le: number): string => {
  return `${le.toFixed(1)} years`;
};

// Format crude birth rate hint - show exact value
const formatCBR = (cbr: number): string => {
  return `${cbr.toFixed(1)} per 1,000`;
};

// Generate hints in order based on incorrect guess count
export const generateHint = (
  country: CountryData,
  guessNumber: number
): Hint | null => {
  // guessNumber is 1-based (1 = first guess, 2 = second guess, etc.)
  // After guess N, we reveal hint N
  switch (guessNumber) {
    case 1:
      return {
        type: 'tfr',
        label: 'Total Fertility Rate (TFR)',
        value: formatTFR(country.totalFertilityRate),
      };
    case 2:
      return {
        type: 'medianAge',
        label: 'Median Age',
        value: formatMedianAge(country.medianAge),
      };
    case 3:
      return {
        type: 'birthsPeak',
        label: 'Year Births Peaked',
        value: formatBirthsPeak(country.yearBirthsPeaked),
      };
    case 4:
      return {
        type: 'lifeExpectancy',
        label: 'Life Expectancy',
        value: formatLifeExpectancy(country.lifeExpectancy),
      };
    case 5:
      return {
        type: 'cbr',
        label: 'Crude Birth Rate (CBR)',
        value: formatCBR(country.crudeBirthRate),
      };
    default:
      return null;
  }
};
