import React, { useState } from 'react';

interface CountryOption {
  code: string;
  name: string;
}

interface CountryInputProps {
  countries: CountryOption[];
  onGuess: (countryCode: string) => void;
  disabled: boolean;
}

export const CountryInput: React.FC<CountryInputProps> = ({
  countries,
  onGuess,
  disabled,
}) => {
  const [selectedCountry, setSelectedCountry] = useState<string>('');

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (selectedCountry) {
      onGuess(selectedCountry);
      setSelectedCountry('');
    }
  };

  return (
    <form onSubmit={handleSubmit} style={{ margin: '20px 0' }}>
      <div style={{ display: 'flex', gap: '10px', justifyContent: 'center', alignItems: 'center' }}>
        <select
          value={selectedCountry}
          onChange={(e) => setSelectedCountry(e.target.value)}
          disabled={disabled}
          style={{
            padding: '10px',
            fontSize: '16px',
            borderRadius: '4px',
            border: '2px solid #ccc',
            minWidth: '250px',
          }}
        >
          <option value="">Select a country...</option>
          {countries.map((country) => (
            <option key={country.code} value={country.code}>
              {country.name}
            </option>
          ))}
        </select>
        <button
          type="submit"
          disabled={disabled || !selectedCountry}
          style={{
            padding: '10px 20px',
            fontSize: '16px',
            backgroundColor: disabled || !selectedCountry ? '#ccc' : '#4CAF50',
            color: 'white',
            border: 'none',
            borderRadius: '4px',
            cursor: disabled || !selectedCountry ? 'not-allowed' : 'pointer',
          }}
        >
          Guess
        </button>
      </div>
    </form>
  );
};
