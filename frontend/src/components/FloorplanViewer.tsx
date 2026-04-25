import React from 'react';
import { CameraPose } from '../types';
import { CameraMarker } from './CameraMarker';

type Props = {
  width: number;
  height: number;
  floorplanUrl: string;
  poses: CameraPose[];
};

function toRad(deg: number) {
  return (deg * Math.PI) / 180;
}

export function FloorplanViewer({ width, height, floorplanUrl, poses }: Props) {
  return (
    <div style={{ position: 'relative', width, height, border: '1px solid #ddd' }}>
      <img src={floorplanUrl} alt="floorplan" style={{ width, height, objectFit: 'contain', position: 'absolute' }} />
      <svg width={width} height={height} style={{ position: 'absolute', left: 0, top: 0 }}>
        {poses.map((pose) => {
          const rayLen = 80;
          const left = toRad(pose.orientation_degrees - pose.fov_degrees / 2);
          const right = toRad(pose.orientation_degrees + pose.fov_degrees / 2);
          const p = pose.position;
          const lx = p.x + rayLen * Math.cos(left);
          const ly = p.y + rayLen * Math.sin(left);
          const rx = p.x + rayLen * Math.cos(right);
          const ry = p.y + rayLen * Math.sin(right);
          return (
            <g key={pose.image_id}>
              <polygon points={`${p.x},${p.y} ${lx},${ly} ${rx},${ry}`} fill="rgba(255,165,0,0.2)" stroke="orange" />
              <CameraMarker x={p.x} y={p.y} confidence={pose.confidence} label={pose.image_id} />
            </g>
          );
        })}
      </svg>
    </div>
  );
}
