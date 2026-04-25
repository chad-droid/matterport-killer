import React, { useEffect, useMemo, useState } from 'react';
import { analyze, createProject, overlayUrl, uploadFloorplan, uploadImages } from './api';
import { AnalyzeResponse } from './types';
import { UploadPanel } from './components/UploadPanel';
import { FloorplanViewer } from './components/FloorplanViewer';
import { ImageResultPanel } from './components/ImageResultPanel';

export default function App() {
  const [projectId, setProjectId] = useState<string>('');
  const [status, setStatus] = useState<string>('');
  const [result, setResult] = useState<AnalyzeResponse | null>(null);

  useEffect(() => {
    createProject().then(setProjectId);
  }, []);

  const floorplanUrl = useMemo(() => (projectId ? overlayUrl(projectId) : ''), [projectId]);

  const onFloorplan = async (file: File) => {
    if (!projectId) return;
    setStatus('Uploading floorplan...');
    await uploadFloorplan(projectId, file);
    setStatus('Floorplan uploaded');
  };

  const onImages = async (files: File[]) => {
    if (!projectId) return;
    setStatus('Uploading images...');
    await uploadImages(projectId, files);
    setStatus(`Uploaded ${files.length} images`);
  };

  const onAnalyze = async () => {
    if (!projectId) return;
    setStatus('Analyzing...');
    const res = await analyze(projectId);
    setResult(res);
    setStatus('Complete');
  };

  return (
    <main style={{ fontFamily: 'Inter, sans-serif', padding: 16, display: 'grid', gap: 16 }}>
      <h1>Floorplan Camera Pose Estimator MVP</h1>
      <div>Project: {projectId || 'creating...'}</div>
      <UploadPanel onFloorplan={onFloorplan} onImages={onImages} onAnalyze={onAnalyze} disabled={!projectId} />
      <div>{status}</div>
      {result && (
        <>
          <FloorplanViewer
            width={Math.min(result.floorplan.width, 900)}
            height={Math.min(result.floorplan.height, 600)}
            floorplanUrl={floorplanUrl}
            poses={result.camera_poses}
          />
          <ImageResultPanel poses={result.camera_poses} />
          <a href={`http://localhost:8000/projects/${projectId}/results`} target="_blank" rel="noreferrer">Export JSON</a>
        </>
      )}
    </main>
  );
}
