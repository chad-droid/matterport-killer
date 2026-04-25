# Matterport Killer MVP (Local Test Guide)

This repo contains a deterministic MVP that auto-estimates likely camera poses for real-estate photos on a floorplan.

## Why your shell failed (`cd backend`, `python`, `pip`, `uvicorn` not found)
You ran setup from your home directory (`~`) instead of the cloned repo, and your machine currently doesn’t have `python` on PATH.

Use:
- `python3` (not `python`) on macOS
- `pip3` or `python3 -m pip`
- `cd` into the repository folder first

---

## 0) Prerequisites (macOS)
Install Homebrew if needed, then install runtime dependencies:

```bash
brew install python@3.11 node
```

Confirm tools exist:

```bash
python3 --version
pip3 --version
node --version
npm --version
```

(Optional OCR improvement)
```bash
brew install tesseract
```

---

## 1) Clone repo + enter it

```bash
cd ~
git clone <YOUR_REPO_URL> matterport-killer
cd matterport-killer
pwd
```

`pwd` should end with `/matterport-killer`.

---

## 2) Start backend
From repo root:

```bash
cd backend
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
python -m uvicorn app.main:app --reload --port 8000
```

Backend health check (new terminal):

```bash
curl http://localhost:8000/health
```

Expected:

```json
{"status":"ok"}
```

---

## 3) Start frontend
In another terminal (from repo root):

```bash
cd ~/matterport-killer/frontend
npm install
npm run dev
```

Open `http://localhost:5173`.

---

## 4) Test full flow in UI
1. Upload floorplan (`.png/.jpg/.jpeg/.pdf`).
2. Upload multiple photos.
3. Click **Analyze Automatically**.
4. Open JSON export link in the UI.

No manual placement is required.

### Optional shortcuts
From repo root:

```bash
make backend-setup
make backend-run
make frontend-setup
make frontend-run
```

---

## 5) API smoke test (optional)

```bash
PROJECT_ID=$(curl -s -X POST http://localhost:8000/projects | python3 -c "import sys, json; print(json.load(sys.stdin)['id'])")

curl -s -X POST "http://localhost:8000/projects/$PROJECT_ID/floorplan" \
  -F "file=@/absolute/path/to/floorplan.png"

curl -s -X POST "http://localhost:8000/projects/$PROJECT_ID/images" \
  -F "files=@/absolute/path/to/photo1.jpg" \
  -F "files=@/absolute/path/to/photo2.jpg"

curl -s -X POST "http://localhost:8000/projects/$PROJECT_ID/analyze" | python3 -m json.tool | head -n 60
curl -s "http://localhost:8000/projects/$PROJECT_ID/results" | python3 -m json.tool | head -n 80
```

---

## Troubleshooting quick map
- `cd: no such file or directory: backend`  
  → You are not in repo root. Run `cd ~/matterport-killer` first.
- `zsh: command not found: python`  
  → Use `python3` or install Python via Homebrew.
- `zsh: command not found: pip`  
  → Use `python3 -m pip`.
- `zsh: command not found: uvicorn`  
  → Activate venv and run `python -m uvicorn ...` after installing requirements.

---

## Notes
- PDF floorplans are rasterized from the first page using `pypdfium2`.
- If local tesseract is not installed, room extraction falls back to deterministic inferred regions.
- Data is stored under `backend/data/projects/`.
