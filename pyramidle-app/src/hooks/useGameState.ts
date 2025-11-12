import { useState, useEffect } from 'react';
import { GameState, CountryData, Hint } from '../types';
import { generateHint } from '../utils/hintGenerator';

interface UseGameStateReturn extends GameState {
  makeGuess: (countryCode: string) => void;
  resetGame: () => void;
  nextCountry: () => void;
}

export const useGameState = (
  availableCountries: CountryData[],
  initialCountryIndex: number = 0
): UseGameStateReturn => {
  const [currentCountryIndex, setCurrentCountryIndex] = useState(initialCountryIndex);
  const [targetCountry, setTargetCountry] = useState<CountryData>(
    availableCountries[initialCountryIndex]
  );
  const [guesses, setGuesses] = useState<string[]>([]);
  const [hintsRevealed, setHintsRevealed] = useState<Hint[]>([]);
  const [gameStatus, setGameStatus] = useState<'playing' | 'won' | 'lost'>('playing');
  const [currentGuess, setCurrentGuess] = useState<number>(0);

  // Update target country when index changes
  useEffect(() => {
    if (availableCountries.length > 0) {
      setTargetCountry(availableCountries[currentCountryIndex]);
    }
  }, [currentCountryIndex, availableCountries]);

  const makeGuess = (countryCode: string) => {
    if (gameStatus !== 'playing' || currentGuess >= 5) {
      return;
    }

    const newGuesses = [...guesses, countryCode];
    setGuesses(newGuesses);
    setCurrentGuess(currentGuess + 1);

    // Check if correct
    if (countryCode === targetCountry.code) {
      setGameStatus('won');
      return;
    }

    // Check if out of guesses
    if (newGuesses.length >= 5) {
      setGameStatus('lost');
      return;
    }

    // Add hint after incorrect guess
    const newHint = generateHint(targetCountry, newGuesses.length);
    if (newHint) {
      setHintsRevealed([...hintsRevealed, newHint]);
    }
  };

  const resetGame = () => {
    setGuesses([]);
    setHintsRevealed([]);
    setGameStatus('playing');
    setCurrentGuess(0);
  };

  const nextCountry = () => {
    const nextIndex = (currentCountryIndex + 1) % availableCountries.length;
    setCurrentCountryIndex(nextIndex);
    resetGame();
  };

  return {
    targetCountry,
    guesses,
    hintsRevealed,
    gameStatus,
    currentGuess,
    makeGuess,
    resetGame,
    nextCountry,
  };
};
