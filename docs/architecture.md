# Architecture

## Overview
- **Backend (FastAPI):** file upload APIs, deterministic analysis pipeline, JSON export, overlay rendering.
- **Frontend (React + TypeScript):** upload floorplan/images, trigger analysis, visualize markers/cones, export results.
- **Storage:** local filesystem under `backend/data/projects/{project_id}`.
- **Schema:** JSON schema in `shared/schemas/camera_pose.schema.json`.

## Pipeline Modules
1. `floorplan_service` parses floorplan size and room regions using OCR/fallback.
2. `exif_service` extracts and normalizes EXIF.
3. `image_analysis_service` provides heuristic image-room cues.
4. `room_matching_service` scores room candidates.
5. `fov_service` estimates camera FOV.
6. `pose_candidate_service` generates candidate camera positions and orientations.
7. `pose_scoring_service` ranks candidates and returns best + alternates.
8. `export_service` serializes stable downstream JSON.
