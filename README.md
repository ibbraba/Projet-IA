# CV Analyzer & Job Matching

Application web pour analyser un CV (PDF) et le comparer a une offre d'emploi.

## Prerequis

- Docker + Docker Compose
- Node.js 20+ (pour dev frontend)
- Python 3.11+ (pour dev backend)

## Demarrage rapide (Docker)

1. Copier les variables d'environnement
	 - racine: .env.example -> .env
	 - backend: backend/.env.example -> backend/.env
2. Lancer
	 - docker compose up --build

## Developpement local (optionnel)

- Frontend
	- cd frontend
	- npm install
	- npm run dev

- Backend
	- cd backend
	- python -m venv .venv
	- pip install -r requirements.txt
	- uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

## Structure

- frontend: React + Vite
- backend: FastAPI
- nginx: reverse proxy
- docs: documentation

## Notes

Les fichiers contiennent des placeholders. Le code sera ajoute ensuite.
