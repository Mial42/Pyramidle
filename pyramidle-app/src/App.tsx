import { useState, useEffect, useMemo } from 'react';
import type { CountryData } from './types';
import { PopulationPyramid } from './components/PopulationPyramid';
import { CountryInput } from './components/CountryInput';
import { GuessGrid } from './components/GuessGrid';
// import { TestModeControls } from './components/TestModeControls';
import { useGameState } from './hooks/useGameState';
import { selectDailyCountry } from './utils/dailyCountry';
import './App.css';

function App() {
  const [countries, setCountries] = useState<CountryData[]>([]);
  const [countryList, setCountryList] = useState<Array<{ code: string; name: string }>>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  // Load country data
  useEffect(() => {
    const loadData = async () => {
      try {
        // Load country list
        const listResponse = await fetch('/data/countries.json');
        const list = await listResponse.json();
        setCountryList(list);

        // Load all country data
        const countryDataPromises = list.map(async (country: { code: string }) => {
          const response = await fetch(`/data/countries/${country.code}.json`);
          return response.json();
        });

        const loadedCountries = await Promise.all(countryDataPromises);
        setCountries(loadedCountries);
        setLoading(false);
      } catch (err) {
        setError('Failed to load country data');
        setLoading(false);
        console.error(err);
      }
    };

    loadData();
  }, []);

  // Select today's country (same for all users, changes daily)
  // Weighted by log-population with 100M cap to avoid always selecting largest countries
  const dailyCountryIndex = useMemo(() => {
    if (countries.length === 0) return 0;
    return selectDailyCountry(countries);
  }, [countries]);

  const {
    targetCountry,
    guesses,
    hintsRevealed,
    gameStatus,
    makeGuess,
    // resetGame, // Only needed for test mode
    // nextCountry, // Only needed for test mode
  } = useGameState(countries, dailyCountryIndex);

  if (loading) {
    return (
      <div style={{ textAlign: 'center', padding: '50px' }}>
        <h2>Loading Pyramidle...</h2>
      </div>
    );
  }

  if (error) {
    return (
      <div style={{ textAlign: 'center', padding: '50px', color: 'red' }}>
        <h2>Error: {error}</h2>
      </div>
    );
  }

  if (!targetCountry) {
    return (
      <div style={{ textAlign: 'center', padding: '50px' }}>
        <h2>No country data available</h2>
      </div>
    );
  }

  // Create country name mapping
  const countryNames = countryList.reduce((acc, country) => {
    acc[country.code] = country.name;
    return acc;
  }, {} as Record<string, string>);

  return (
    <div style={{ padding: '20px', maxWidth: '1200px', margin: '0 auto' }}>
      <header style={{ textAlign: 'center', marginBottom: '30px' }}>
        <h1 style={{ fontSize: '48px', margin: '20px 0 10px' }}>🌍 Pyramidle</h1>
        <p style={{ fontSize: '18px', color: '#666' }}>
          Guess the country from its population pyramid!
        </p>
        <p style={{ fontSize: '14px', color: '#999' }}>
          You have 6 guesses. Each wrong guess reveals a hint.
        </p>
      </header>

      {/* Game Status Message */}
      {gameStatus === 'won' && (
        <div style={{
          textAlign: 'center',
          padding: '20px',
          backgroundColor: '#d4edda',
          borderRadius: '8px',
          border: '2px solid #28a745',
          color: '#155724',
          marginBottom: '20px',
          fontSize: '20px',
          fontWeight: 'bold',
        }}>
          🎉 Congratulations! You guessed {countryNames[targetCountry.code]} in {guesses.length} {guesses.length === 1 ? 'guess' : 'guesses'}!
        </div>
      )}

      {gameStatus === 'lost' && (
        <div style={{
          textAlign: 'center',
          padding: '20px',
          backgroundColor: '#f8d7da',
          borderRadius: '8px',
          border: '2px solid #dc3545',
          color: '#721c24',
          marginBottom: '20px',
          fontSize: '20px',
          fontWeight: 'bold',
        }}>
          Game Over! The country was {countryNames[targetCountry.code]}.
        </div>
      )}

      {/* Population Pyramid */}
      <PopulationPyramid
        pyramidData={targetCountry.pyramid}
        totalPopulation={targetCountry.population}
      />

      {/* Country Input */}
      <CountryInput
        countries={countryList}
        onGuess={makeGuess}
        disabled={gameStatus !== 'playing'}
      />

      {/* Guess Grid with Hints */}
      <GuessGrid
        guesses={guesses}
        hints={hintsRevealed}
        countryNames={countryNames}
        targetCountry={targetCountry.code}
        maxGuesses={6}
      />

      {/* Test Mode Controls - Uncomment to enable test mode
      <TestModeControls
        onNextCountry={nextCountry}
        onReset={resetGame}
        gameStatus={gameStatus}
      />
      */}

      <footer style={{ textAlign: 'center', marginTop: '50px', color: '#999', fontSize: '14px' }}>
        <p>Inspired by <a href="https://oec.world/en/games/tradle" target="_blank" rel="noopener noreferrer">Tradle</a></p>
        <p>Data from UN Population Division and World Bank</p>
      </footer>
    </div>
  );
}

export default App;
