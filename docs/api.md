# API

## Endpoints

- `POST /projects` → create project id.
- `GET /health` → simple healthcheck.
- `POST /projects/{id}/floorplan` → upload floorplan image/PDF (PDF uses first-page rasterization).
- `POST /projects/{id}/images` → upload batch images and extract EXIF.
- `POST /projects/{id}/analyze` → run full automatic pipeline.
- `GET /projects/{id}/results` → return exported JSON payload.
- `GET /projects/{id}/overlay` → return overlay image with camera markers and FOV cones.

## Local run
```bash
cd backend
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
python -m uvicorn app.main:app --reload --port 8000
```

Frontend should call backend at `http://localhost:8000`.
