import { useState } from 'react';

interface ShareResultsProps {
  date: string;
  guessCount: number | 'X';
  squares: string[];
}

export const ShareResults = ({ date, guessCount, squares }: ShareResultsProps) => {
  const [copied, setCopied] = useState(false);

  const shareText = `#Pyramidle ${date} ${guessCount}/6\n${squares.join('\n')}`;

  const handleShare = async () => {
    try {
      await navigator.clipboard.writeText(shareText);
      setCopied(true);
      setTimeout(() => setCopied(false), 2000);
    } catch (err) {
      console.error('Failed to copy:', err);
    }
  };

  return (
    <div
      style={{
        backgroundColor: '#f8f9fa',
        border: '2px solid #dee2e6',
        borderRadius: '12px',
        padding: '24px',
        margin: '20px auto',
        maxWidth: '400px',
        textAlign: 'center',
      }}
    >
      <h3 style={{ marginTop: 0, marginBottom: '16px', fontSize: '20px' }}>
        Results
      </h3>

      <div
        style={{
          backgroundColor: 'white',
          padding: '16px',
          borderRadius: '8px',
          marginBottom: '16px',
          fontFamily: 'monospace',
          fontSize: '16px',
          lineHeight: '1.8',
          whiteSpace: 'pre-line',
        }}
      >
        <div style={{ fontWeight: 'bold', marginBottom: '8px' }}>
          #Pyramidle {date} {guessCount}/6
        </div>
        {squares.map((line, i) => (
          <div key={i} style={{ letterSpacing: '2px' }}>
            {line}
          </div>
        ))}
      </div>

      <button
        onClick={handleShare}
        style={{
          backgroundColor: copied ? '#28a745' : '#007bff',
          color: 'white',
          border: 'none',
          borderRadius: '8px',
          padding: '12px 24px',
          fontSize: '16px',
          fontWeight: 'bold',
          cursor: 'pointer',
          transition: 'background-color 0.2s',
        }}
      >
        {copied ? '✓ Copied!' : 'Share Result'}
      </button>

      <div style={{ marginTop: '12px', fontSize: '12px', color: '#6c757d' }}>
        🟩 Very close · 🟨 Medium · ⬜ Far
      </div>
      <div style={{ marginTop: '4px', fontSize: '11px', color: '#6c757d' }}>
        Population · TFR · Median Age · Birth Peak · Life Exp · CBR
      </div>
    </div>
  );
};
