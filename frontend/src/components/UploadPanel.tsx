import React from 'react';

type Props = {
  onFloorplan: (file: File) => void;
  onImages: (files: File[]) => void;
  onAnalyze: () => void;
  disabled?: boolean;
};

export function UploadPanel({ onFloorplan, onImages, onAnalyze, disabled }: Props) {
  return (
    <div style={{ display: 'grid', gap: 8 }}>
      <label>
        Floorplan (image/pdf)
        <input type="file" onChange={(e) => e.target.files?.[0] && onFloorplan(e.target.files[0])} />
      </label>
      <label>
        Home images
        <input type="file" multiple onChange={(e) => e.target.files && onImages(Array.from(e.target.files))} />
      </label>
      <button onClick={onAnalyze} disabled={disabled}>Analyze Automatically</button>
    </div>
  );
}
