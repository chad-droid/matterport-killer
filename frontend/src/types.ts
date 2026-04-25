export type UploadResponse = { ok: boolean; uploaded?: number; rooms_detected?: number };

export type CameraPose = {
  image_id: string;
  room_id: string;
  position: { x: number; y: number };
  orientation_degrees: number;
  direction_vector: { dx: number; dy: number };
  fov_degrees: number;
  confidence: number;
  perspective_description: string;
  alternates: Array<{ position: { x: number; y: number }; orientation_degrees: number; confidence: number }>;
  uncertainty_reasons: string[];
};

export type AnalyzeResponse = {
  project_id: string;
  floorplan: { file_path: string; width: number; height: number };
  camera_poses: CameraPose[];
};
