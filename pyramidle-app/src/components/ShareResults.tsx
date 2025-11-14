import { useState, useEffect } from 'react';

interface ShareResultsProps {
  date: string;
  guessCount: number | 'X';
  squares: string[];
  onClose?: () => void;
}

export const ShareResults = ({ date, guessCount, squares, onClose }: ShareResultsProps) => {
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

  // Handle escape key to close modal
  useEffect(() => {
    const handleEscape = (e: KeyboardEvent) => {
      if (e.key === 'Escape' && onClose) {
        onClose();
      }
    };

    document.addEventListener('keydown', handleEscape);
    return () => document.removeEventListener('keydown', handleEscape);
  }, [onClose]);

  // Prevent body scroll when modal is open
  useEffect(() => {
    document.body.style.overflow = 'hidden';
    return () => {
      document.body.style.overflow = 'unset';
    };
  }, []);

  const handleOverlayClick = (e: React.MouseEvent) => {
    // Close if clicking the overlay background (not the modal content)
    if (e.target === e.currentTarget && onClose) {
      onClose();
    }
  };

  return (
    <div
      onClick={handleOverlayClick}
      style={{
        position: 'fixed',
        top: 0,
        left: 0,
        right: 0,
        bottom: 0,
        backgroundColor: 'rgba(0, 0, 0, 0.6)',
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'center',
        zIndex: 1000,
        padding: '20px',
      }}
    >
      <div
        style={{
          backgroundColor: '#f8f9fa',
          border: '2px solid #dee2e6',
          borderRadius: '12px',
          padding: '24px',
          maxWidth: '400px',
          width: '100%',
          textAlign: 'center',
          position: 'relative',
          animation: 'fadeIn 0.2s ease-out',
        }}
      >
        {/* Close button */}
        {onClose && (
          <button
            onClick={onClose}
            style={{
              position: 'absolute',
              top: '12px',
              right: '12px',
              background: 'none',
              border: 'none',
              fontSize: '24px',
              cursor: 'pointer',
              color: '#999',
              lineHeight: 1,
              padding: '4px 8px',
            }}
            aria-label="Close"
          >
            ×
          </button>
        )}

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
          🟩 ≤10 ranks · 🟨 ≤30 ranks · ⬜ ≤60 ranks · 🟥 &gt;60 ranks
        </div>
        <div style={{ marginTop: '4px', fontSize: '11px', color: '#6c757d' }}>
          Population · TFR · Median Age · Birth Peak · Life Exp · CBR
        </div>
      </div>
    </div>
  );
};
