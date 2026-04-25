import React from 'react';

type Props = {
  x: number;
  y: number;
  confidence: number;
  label: string;
};

export function CameraMarker({ x, y, confidence, label }: Props) {
  return (
    <g>
      <circle cx={x} cy={y} r={6} fill="red" />
      <text x={x + 8} y={y - 8} fontSize={12} fill="blue">{label} ({confidence.toFixed(2)})</text>
    </g>
  );
}
