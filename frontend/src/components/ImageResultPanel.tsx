import React from 'react';
import { CameraPose } from '../types';
import { ConfidenceBadge } from './ConfidenceBadge';

export function ImageResultPanel({ poses }: { poses: CameraPose[] }) {
  return (
    <div>
      <h3>Image Pose Results</h3>
      <ul>
        {poses.map((p) => (
          <li key={p.image_id} style={{ marginBottom: 8 }}>
            <b>{p.image_id}</b> → {p.room_id} | {p.orientation_degrees}° | FOV {p.fov_degrees}° | <ConfidenceBadge value={p.confidence} />
            <div style={{ fontSize: 12 }}>{p.perspective_description}</div>
          </li>
        ))}
      </ul>
    </div>
  );
}
