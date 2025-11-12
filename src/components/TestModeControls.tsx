import React from 'react';

interface TestModeControlsProps {
  onNextCountry: () => void;
  onReset: () => void;
  gameStatus: 'playing' | 'won' | 'lost';
}

export const TestModeControls: React.FC<TestModeControlsProps> = ({
  onNextCountry,
  onReset,
  gameStatus,
}) => {
  return (
    <div style={{
      margin: '20px auto',
      maxWidth: '400px',
      padding: '15px',
      backgroundColor: '#fff3cd',
      borderRadius: '8px',
      border: '2px solid #ffc107',
    }}>
      <h3 style={{ marginTop: 0, marginBottom: '15px', fontSize: '16px', color: '#856404' }}>
        🔧 Test Mode
      </h3>
      <div style={{ display: 'flex', gap: '10px', justifyContent: 'center' }}>
        <button
          onClick={onNextCountry}
          style={{
            padding: '10px 20px',
            fontSize: '14px',
            backgroundColor: '#007bff',
            color: 'white',
            border: 'none',
            borderRadius: '4px',
            cursor: 'pointer',
          }}
        >
          Next Country
        </button>
        <button
          onClick={onReset}
          disabled={gameStatus === 'playing' && true}
          style={{
            padding: '10px 20px',
            fontSize: '14px',
            backgroundColor: '#6c757d',
            color: 'white',
            border: 'none',
            borderRadius: '4px',
            cursor: 'pointer',
          }}
        >
          Reset Game
        </button>
      </div>
    </div>
  );
};
