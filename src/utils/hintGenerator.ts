import { CountryData, Hint } from '../types';

// Format TFR hint
const formatTFR = (tfr: number): string => {
  if (tfr < 1.5) return '< 1.5';
  if (tfr < 2.0) return '1.5-2.0';
  if (tfr < 2.5) return '2.0-2.5';
  if (tfr < 3.0) return '2.5-3.0';
  if (tfr < 4.0) return '3.0-4.0';
  if (tfr < 5.0) return '4.0-5.0';
  return '> 5.0';
};

// Format median age hint
const formatMedianAge = (age: number): string => {
  const lower = Math.floor(age / 5) * 5;
  const upper = lower + 5;
  return `${lower}-${upper} years`;
};

// Format births peak year hint
const formatBirthsPeak = (year: number): string => {
  const lower = Math.floor(year / 5) * 5;
  const upper = lower + 5;
  return `${lower}-${upper}`;
};

// Format life expectancy hint
const formatLifeExpectancy = (le: number): string => {
  const lower = Math.floor(le / 5) * 5;
  const upper = lower + 5;
  return `${lower}-${upper} years`;
};

// Format crude birth rate hint
const formatCBR = (cbr: number): string => {
  const lower = Math.floor(cbr / 5) * 5;
  const upper = lower + 5;
  return `${lower}-${upper} per 1,000`;
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
