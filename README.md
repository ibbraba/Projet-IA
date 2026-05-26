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




## Entraînement IA

Tous les tests ont été effectués avec une offre d'emploi de développeur Java.

### 1. Semantic Matcher sans modèle IA

- CV Ange : **25 %**
- CV conseiller de vente : **18 %**
- CV cuisinier : **11 %**

---

### 2. Ajout du modèle IA SentenceTransformer

Modèle utilisé :  
`paraphrase-multilingual-MiniLM-L12-v2`

#### Résultats

- CV Ange : **51 %**
- CV conseiller de vente : **35 %**
- CV cuisinier : **21 %**

### Conclusion

Résultats encore trop imprécis.

---

### 3. Ajout de la méthode `extract_dense_content`

Objectif : filtrer les zones de compétences clés.

#### Résultats

- CV Ange : **64 %**
- CV conseiller de vente : **20 %**
- CV cuisinier : **18 %**

---

### 4. Ajout des *skills multipliers*

Application d’un multiplicateur pour chaque compétence.

#### Premier test

- CV Ange : **45 %**
  - Baisse due à des faux négatifs.

#### Ajustement des multiplicateurs

- CV Ange : **64 %** *(inchangé)*
- CV conseiller de vente : **10 %**
- CV cuisinier : **11 %**

### Conclusion finale

Avec cet entraînement, le modèle reflète désormais beaucoup plus clairement le résultat attendu.