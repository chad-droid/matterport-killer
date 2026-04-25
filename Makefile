.PHONY: backend-setup backend-run frontend-setup frontend-run

backend-setup:
	cd backend && python3 -m venv .venv && . .venv/bin/activate && python -m pip install --upgrade pip && python -m pip install -r requirements.txt

backend-run:
	cd backend && . .venv/bin/activate && python -m uvicorn app.main:app --reload --port 8000

frontend-setup:
	cd frontend && npm install

frontend-run:
	cd frontend && npm run dev
