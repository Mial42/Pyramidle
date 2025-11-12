import React, { useState, useRef, useEffect } from 'react';

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
  const [inputValue, setInputValue] = useState<string>('');
  const [selectedCountry, setSelectedCountry] = useState<string>('');
  const [showDropdown, setShowDropdown] = useState<boolean>(false);
  const [highlightedIndex, setHighlightedIndex] = useState<number>(0);
  const inputRef = useRef<HTMLInputElement>(null);
  const dropdownRef = useRef<HTMLDivElement>(null);

  // Sort countries alphabetically by code
  const sortedCountries = [...countries].sort((a, b) => a.code.localeCompare(b.code));

  // Filter countries based on input (substring match on name or code)
  const filteredCountries = sortedCountries.filter((country) => {
    const searchTerm = inputValue.toLowerCase();
    return (
      country.name.toLowerCase().includes(searchTerm) ||
      country.code.toLowerCase().includes(searchTerm)
    );
  });

  // Handle click outside to close dropdown
  useEffect(() => {
    const handleClickOutside = (event: MouseEvent) => {
      if (
        dropdownRef.current &&
        !dropdownRef.current.contains(event.target as Node) &&
        inputRef.current &&
        !inputRef.current.contains(event.target as Node)
      ) {
        setShowDropdown(false);
      }
    };

    document.addEventListener('mousedown', handleClickOutside);
    return () => document.removeEventListener('mousedown', handleClickOutside);
  }, []);

  const handleInputChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    setInputValue(e.target.value);
    setSelectedCountry('');
    setShowDropdown(true);
    setHighlightedIndex(0);
  };

  const handleCountrySelect = (country: CountryOption) => {
    setInputValue(`${country.code} - ${country.name}`);
    setSelectedCountry(country.code);
    setShowDropdown(false);
  };

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (selectedCountry) {
      onGuess(selectedCountry);
      setInputValue('');
      setSelectedCountry('');
    }
  };

  const handleKeyDown = (e: React.KeyboardEvent) => {
    if (!showDropdown) {
      if (e.key === 'ArrowDown' || e.key === 'ArrowUp') {
        setShowDropdown(true);
      }
      return;
    }

    switch (e.key) {
      case 'ArrowDown':
        e.preventDefault();
        setHighlightedIndex((prev) =>
          prev < filteredCountries.length - 1 ? prev + 1 : prev
        );
        break;
      case 'ArrowUp':
        e.preventDefault();
        setHighlightedIndex((prev) => (prev > 0 ? prev - 1 : 0));
        break;
      case 'Enter':
        e.preventDefault();
        if (filteredCountries.length > 0 && highlightedIndex < filteredCountries.length) {
          handleCountrySelect(filteredCountries[highlightedIndex]);
        }
        break;
      case 'Escape':
        setShowDropdown(false);
        break;
    }
  };

  return (
    <form onSubmit={handleSubmit} style={{ margin: '20px 0' }}>
      <div style={{ display: 'flex', gap: '10px', justifyContent: 'center', alignItems: 'center' }}>
        <div style={{ position: 'relative', minWidth: '350px' }}>
          <input
            ref={inputRef}
            type="text"
            value={inputValue}
            onChange={handleInputChange}
            onKeyDown={handleKeyDown}
            onFocus={() => setShowDropdown(true)}
            disabled={disabled}
            placeholder="Type country name or code..."
            style={{
              width: '100%',
              padding: '10px',
              fontSize: '16px',
              borderRadius: '4px',
              border: '2px solid #ccc',
              boxSizing: 'border-box',
            }}
          />

          {showDropdown && filteredCountries.length > 0 && (
            <div
              ref={dropdownRef}
              style={{
                position: 'absolute',
                top: '100%',
                left: 0,
                right: 0,
                maxHeight: '300px',
                overflowY: 'auto',
                backgroundColor: 'white',
                border: '2px solid #ccc',
                borderTop: 'none',
                borderRadius: '0 0 4px 4px',
                boxShadow: '0 4px 6px rgba(0,0,0,0.1)',
                zIndex: 1000,
              }}
            >
              {filteredCountries.map((country, index) => (
                <div
                  key={country.code}
                  onClick={() => handleCountrySelect(country)}
                  style={{
                    padding: '10px',
                    cursor: 'pointer',
                    backgroundColor: index === highlightedIndex ? '#e3f2fd' : 'white',
                    borderBottom: index < filteredCountries.length - 1 ? '1px solid #eee' : 'none',
                  }}
                  onMouseEnter={() => setHighlightedIndex(index)}
                >
                  <strong>{country.code}</strong> - {country.name}
                </div>
              ))}
            </div>
          )}
        </div>

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
