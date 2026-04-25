import { AnalyzeResponse, UploadResponse } from './types';

const API_BASE = 'http://localhost:8000';

export async function createProject(): Promise<string> {
  const res = await fetch(`${API_BASE}/projects`, { method: 'POST' });
  const data = await res.json();
  return data.id;
}

export async function uploadFloorplan(projectId: string, file: File): Promise<UploadResponse> {
  const fd = new FormData();
  fd.append('file', file);
  const res = await fetch(`${API_BASE}/projects/${projectId}/floorplan`, { method: 'POST', body: fd });
  return res.json();
}

export async function uploadImages(projectId: string, files: File[]): Promise<UploadResponse> {
  const fd = new FormData();
  files.forEach((f) => fd.append('files', f));
  const res = await fetch(`${API_BASE}/projects/${projectId}/images`, { method: 'POST', body: fd });
  return res.json();
}

export async function analyze(projectId: string): Promise<AnalyzeResponse> {
  const res = await fetch(`${API_BASE}/projects/${projectId}/analyze`, { method: 'POST' });
  return res.json();
}

export function overlayUrl(projectId: string): string {
  return `${API_BASE}/projects/${projectId}/overlay`;
}
