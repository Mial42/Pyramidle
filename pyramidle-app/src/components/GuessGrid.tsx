import React from 'react';
import type { Hint } from '../types';

interface GuessGridProps {
  guesses: string[];
  hints: Hint[];
  countryNames: Record<string, string>;
  targetCountry: string;
  maxGuesses: number;
}

export const GuessGrid: React.FC<GuessGridProps> = ({
  guesses,
  hints,
  countryNames,
  targetCountry,
  maxGuesses,
}) => {
  // Create array of all guess slots (filled and empty)
  const guessSlots = Array.from({ length: maxGuesses }, (_, index) => {
    const guessCode = guesses[index];
    const hint = hints[index];
    const isCorrect = guessCode === targetCountry;
    const isEmpty = !guessCode;

    return (
      <div
        key={index}
        style={{
          display: 'flex',
          gap: '10px',
          marginBottom: '8px',
          alignItems: 'center',
        }}
      >
        {/* Guess number */}
        <div
          style={{
            width: '30px',
            textAlign: 'center',
            fontWeight: 'bold',
            color: '#666',
          }}
        >
          {index + 1}
        </div>

        {/* Guess box */}
        <div
          style={{
            flex: '0 0 200px',
            padding: '12px',
            borderRadius: '6px',
            border: isEmpty ? '2px dashed #ccc' : `2px solid ${isCorrect ? '#28a745' : '#dc3545'}`,
            backgroundColor: isEmpty ? '#f8f9fa' : isCorrect ? '#d4edda' : '#f8d7da',
            color: isEmpty ? '#999' : isCorrect ? '#155724' : '#721c24',
            fontWeight: isEmpty ? 'normal' : 'bold',
            textAlign: 'center',
          }}
        >
          {isEmpty ? '—' : countryNames[guessCode] || guessCode}
          {isCorrect && ' ✓'}
        </div>

        {/* Hint box */}
        <div
          style={{
            flex: 1,
            padding: '12px',
            borderRadius: '6px',
            border: hint ? '2px solid #ffc107' : '2px dashed #e0e0e0',
            backgroundColor: hint ? '#fff3cd' : '#fafafa',
            color: hint ? '#856404' : '#ccc',
            fontSize: '14px',
            minHeight: '44px',
            display: 'flex',
            alignItems: 'center',
          }}
        >
          {hint ? (
            <>
              <strong style={{ marginRight: '8px' }}>{hint.label}:</strong>
              <span>{hint.value}</span>
            </>
          ) : (
            <span style={{ fontStyle: 'italic' }}>Hint will appear here</span>
          )}
        </div>
      </div>
    );
  });

  return (
    <div style={{
      margin: '20px auto',
      maxWidth: '900px',
      padding: '20px',
      backgroundColor: '#fff',
      borderRadius: '12px',
      border: '2px solid #ddd',
      boxShadow: '0 2px 8px rgba(0,0,0,0.1)',
    }}>
      {guessSlots}
    </div>
  );
};
