import React from 'react';
import type { Hint } from '../types';

interface HintDisplayProps {
  hints: Hint[];
}

export const HintDisplay: React.FC<HintDisplayProps> = ({ hints }) => {
  if (hints.length === 0) {
    return null;
  }

  return (
    <div style={{
      margin: '20px auto',
      maxWidth: '600px',
      padding: '15px',
      backgroundColor: '#f5f5f5',
      borderRadius: '8px',
      border: '2px solid #ddd',
    }}>
      <h3 style={{ marginTop: 0, marginBottom: '15px', fontSize: '18px' }}>Hints Revealed:</h3>
      <div style={{ display: 'flex', flexDirection: 'column', gap: '10px' }}>
        {hints.map((hint, index) => (
          <div
            key={index}
            style={{
              padding: '10px',
              backgroundColor: 'white',
              borderRadius: '4px',
              border: '1px solid #ccc',
            }}
          >
            <strong>{hint.label}:</strong> {hint.value}
          </div>
        ))}
      </div>
    </div>
  );
};
