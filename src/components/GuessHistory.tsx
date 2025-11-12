import React from 'react';

interface GuessHistoryProps {
  guesses: string[];
  countryNames: Record<string, string>;
  targetCountry: string;
  gameStatus: 'playing' | 'won' | 'lost';
}

export const GuessHistory: React.FC<GuessHistoryProps> = ({
  guesses,
  countryNames,
  targetCountry,
  gameStatus,
}) => {
  if (guesses.length === 0) {
    return null;
  }

  return (
    <div style={{
      margin: '20px auto',
      maxWidth: '400px',
      padding: '15px',
      backgroundColor: '#f9f9f9',
      borderRadius: '8px',
      border: '2px solid #ddd',
    }}>
      <h3 style={{ marginTop: 0, marginBottom: '15px', fontSize: '18px' }}>
        Your Guesses ({guesses.length}/5):
      </h3>
      <div style={{ display: 'flex', flexDirection: 'column', gap: '8px' }}>
        {guesses.map((code, index) => {
          const isCorrect = code === targetCountry;
          return (
            <div
              key={index}
              style={{
                padding: '10px',
                backgroundColor: isCorrect ? '#d4edda' : '#f8d7da',
                borderRadius: '4px',
                border: `2px solid ${isCorrect ? '#28a745' : '#dc3545'}`,
                color: isCorrect ? '#155724' : '#721c24',
              }}
            >
              {index + 1}. {countryNames[code] || code}
              {isCorrect && ' ✓'}
            </div>
          );
        })}
      </div>
      {gameStatus === 'lost' && (
        <div style={{
          marginTop: '15px',
          padding: '10px',
          backgroundColor: '#fff3cd',
          borderRadius: '4px',
          border: '2px solid #ffc107',
          color: '#856404',
          textAlign: 'center',
        }}>
          The answer was: <strong>{countryNames[targetCountry]}</strong>
        </div>
      )}
    </div>
  );
};
