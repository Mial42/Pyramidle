import type { CountryData } from '../types';

/**
 * Get the number of days since the epoch (Jan 1, 1970)
 * This serves as a daily seed that's the same for all users worldwide
 */
const getDailySeed = (): number => {
  const now = new Date();
  // Use UTC to ensure same date worldwide
  const utcDate = Date.UTC(now.getUTCFullYear(), now.getUTCMonth(), now.getUTCDate());
  const epoch = Date.UTC(1970, 0, 1);
  return Math.floor((utcDate - epoch) / (1000 * 60 * 60 * 24));
};

/**
 * Seeded random number generator (Mulberry32)
 * Returns a deterministic random number between 0 and 1
 */
const seededRandom = (seed: number): number => {
  let state = seed + 0x6D2B79F5;
  state = Math.imul(state ^ (state >>> 15), state | 1);
  state ^= state + Math.imul(state ^ (state >>> 7), state | 61);
  return ((state ^ (state >>> 14)) >>> 0) / 4294967296;
};

/**
 * Calculate weight for a country based on log-population
 * Population is capped at 100M to avoid always selecting the largest countries
 */
const getCountryWeight = (population: number): number => {
  const cappedPopulation = Math.min(population, 100_000_000);
  // Use log to compress the range - makes small countries more likely
  // Add 1 to avoid log(0) issues
  return Math.log(cappedPopulation + 1);
};

/**
 * Select a country for today using weighted random selection
 * All users worldwide will get the same country on the same day
 */
export const selectDailyCountry = (countries: CountryData[]): number => {
  if (countries.length === 0) {
    return 0;
  }

  const seed = getDailySeed();

  // Calculate weights for all countries
  const weights = countries.map(country => getCountryWeight(country.population));
  const totalWeight = weights.reduce((sum, weight) => sum + weight, 0);

  // Generate random value between 0 and totalWeight
  const randomValue = seededRandom(seed) * totalWeight;

  // Select country based on weighted random value
  let cumulativeWeight = 0;
  for (let i = 0; i < countries.length; i++) {
    cumulativeWeight += weights[i];
    if (randomValue <= cumulativeWeight) {
      return i;
    }
  }

  // Fallback (should never reach here)
  return countries.length - 1;
};
