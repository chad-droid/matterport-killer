import React from 'react';

export function ConfidenceBadge({ value }: { value: number }) {
  const color = value > 0.75 ? '#198754' : value > 0.55 ? '#ffc107' : '#dc3545';
  return <span style={{ background: color, color: 'white', padding: '2px 6px', borderRadius: 6 }}>{value.toFixed(2)}</span>;
}
