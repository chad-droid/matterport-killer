from pathlib import Path

DATA_DIR = Path(__file__).resolve().parents[2] / "data"
PROJECTS_DIR = DATA_DIR / "projects"
UPLOADS_DIR = DATA_DIR / "uploads"

for directory in (DATA_DIR, PROJECTS_DIR, UPLOADS_DIR):
    directory.mkdir(parents=True, exist_ok=True)
