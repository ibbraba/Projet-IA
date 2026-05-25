# 🎯 CV Analyzer & Job Matching System - Architecture Complète

## 📑 Table des Matières

1. [Vue d'ensemble](#vue-densemble)
2. [Architecture Technique](#architecture-technique)
3. [Structure du Projet](#structure-du-projet)
4. [Stack Technique](#stack-technique)
5. [Pipeline de Traitement](#pipeline-de-traitement)
6. [Modèles de Données](#modèles-de-données)
7. [API Endpoints](#api-endpoints)
8. [Composants Frontend](#composants-frontend)
9. [Services Backend](#services-backend)
10. [Configuration Docker](#configuration-docker)
11. [Étapes d'Implémentation](#étapes-dimplémentation)
12. [Guide de Démarrage](#guide-de-démarrage)
13. [Tests & Qualité](#tests--qualité)
14. [Déploiement](#déploiement)
15. [Roadmap & Évolutions](#roadmap--évolutions)

---

## 🎨 Vue d'ensemble

### Objectif du Projet
Créer une application web permettant d'analyser automatiquement la compatibilité entre un CV (PDF) et une offre d'emploi, en fournissant :
- Un score de matching détaillé
- Une visualisation interactive des compétences (radar chart)
- Des suggestions concrètes d'amélioration du CV
- Une analyse des points forts et faibles

### Caractéristiques Principales
- ✅ Upload de CV au format PDF
- ✅ Analyse NLP avancée avec spaCy
- ✅ Matching sémantique avec sentence-transformers
- ✅ Génération de suggestions par LLM (Claude/GPT)
- ✅ Visualisations interactives (Chart.js)
- ✅ Interface moderne et responsive
- ✅ Architecture microservices avec Docker

---

## 🏗️ Architecture Technique

### Diagramme d'Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                         NGINX (Port 80)                      │
│                      Reverse Proxy / Load Balancer           │
└───────────────┬─────────────────────────┬───────────────────┘
                │                         │
        ┌───────▼────────┐        ┌──────▼───────┐
        │   FRONTEND     │        │   BACKEND    │
        │  React + Vite  │◄──────►│   FastAPI    │
        │   Port 3000    │  REST  │   Port 8000  │
        └────────────────┘  API   └──────┬───────┘
                                         │
                    ┌────────────────────┼────────────────────┐
                    │                    │                    │
            ┌───────▼────────┐  ┌────────▼────────┐  ┌───────▼────────┐
            │   PostgreSQL   │  │      Redis      │  │   AI Models    │
            │   Port 5432    │  │   Port 6379     │  │  (spaCy, ST)   │
            │  (Persistence) │  │    (Cache)      │  │   (In-Memory)  │
            └────────────────┘  └─────────────────┘  └────────────────┘
```

### Flux de Données

```
User Upload CV (PDF) + Job Description
            ↓
    Frontend Validation
            ↓
    POST /api/analyze
            ↓
    Backend FastAPI
            ↓
    ┌───────────────────────────────────┐
    │  1. PDF Text Extraction           │
    │     (PyPDF2 + pdfplumber)         │
    └───────────┬───────────────────────┘
                ↓
    ┌───────────────────────────────────┐
    │  2. NLP Processing                │
    │     - Tokenization (spaCy)        │
    │     - Entity Extraction (NER)     │
    │     - Skills Detection            │
    └───────────┬───────────────────────┘
                ↓
    ┌───────────────────────────────────┐
    │  3. Semantic Matching             │
    │     - Generate Embeddings (ST)    │
    │     - Cosine Similarity           │
    │     - Calculate Scores            │
    └───────────┬───────────────────────┘
                ↓
    ┌───────────────────────────────────┐
    │  4. LLM Suggestions               │
    │     - Claude API Call             │
    │     - Generate Improvements       │
    └───────────┬───────────────────────┘
                ↓
    ┌───────────────────────────────────┐
    │  5. Response Formatting           │
    │     - Radar Chart Data            │
    │     - Strengths/Weaknesses        │
    │     - Actionable Suggestions      │
    └───────────┬───────────────────────┘
                ↓
    JSON Response to Frontend
            ↓
    Visualization Rendering
```

---

## 📂 Structure du Projet

```
cv-analyzer-matching/
│
├── docker-compose.yml              # Orchestration des services
├── .env.example                    # Template des variables d'environnement
├── .gitignore                      # Fichiers à ignorer par Git
├── README.md                       # Documentation principale
├── Makefile                        # Commandes utilitaires
│
├── frontend/                       # Application React
│   ├── Dockerfile
│   ├── .dockerignore
│   ├── package.json
│   ├── package-lock.json
│   ├── tsconfig.json
│   ├── vite.config.ts
│   ├── tailwind.config.js
│   ├── postcss.config.js
│   ├── index.html
│   │
│   ├── public/
│   │   ├── favicon.ico
│   │   └── assets/
│   │
│   └── src/
│       ├── main.tsx                # Entry point
│       ├── App.tsx                 # App principale
│       ├── vite-env.d.ts
│       │
│       ├── components/             # Composants React
│       │   ├── layout/
│       │   │   ├── Header.tsx
│       │   │   ├── Footer.tsx
│       │   │   └── Layout.tsx
│       │   │
│       │   ├── upload/
│       │   │   ├── CVUploader.tsx
│       │   │   └── JobDescriptionInput.tsx
│       │   │
│       │   ├── analysis/
│       │   │   ├── MatchingScore.tsx
│       │   │   ├── SkillsRadarChart.tsx
│       │   │   ├── ScoreGauge.tsx
│       │   │   ├── CategoryBreakdown.tsx
│       │   │   └── KeywordsCloud.tsx
│       │   │
│       │   ├── results/
│       │   │   ├── StrengthsWeaknesses.tsx
│       │   │   ├── ImprovementSuggestions.tsx
│       │   │   └── ExportReport.tsx
│       │   │
│       │   └── ui/                 # Composants UI réutilisables
│       │       ├── Button.tsx
│       │       ├── Card.tsx
│       │       ├── Badge.tsx
│       │       ├── Progress.tsx
│       │       └── Spinner.tsx
│       │
│       ├── services/               # Services API
│       │   ├── api.ts              # Client API principal
│       │   └── storage.ts          # LocalStorage utilities
│       │
│       ├── hooks/                  # Custom hooks
│       │   ├── useAnalysis.ts
│       │   ├── useFileUpload.ts
│       │   └── useLocalStorage.ts
│       │
│       ├── types/                  # TypeScript types
│       │   ├── index.ts
│       │   ├── api.types.ts
│       │   └── chart.types.ts
│       │
│       ├── utils/                  # Utilitaires
│       │   ├── validators.ts
│       │   ├── formatters.ts
│       │   └── constants.ts
│       │
│       ├── styles/                 # Styles globaux
│       │   ├── globals.css
│       │   └── animations.css
│       │
│       └── assets/                 # Images, icons
│           └── images/
│
├── backend/                        # API FastAPI
│   ├── Dockerfile
│   ├── .dockerignore
│   ├── requirements.txt
│   ├── requirements-dev.txt
│   ├── pytest.ini
│   ├── .env.example
│   │
│   ├── app/
│   │   ├── __init__.py
│   │   ├── main.py                 # Entry point FastAPI
│   │   ├── config.py               # Configuration
│   │   ├── dependencies.py         # Dépendances FastAPI
│   │   │
│   │   ├── api/                    # Routes API
│   │   │   ├── __init__.py
│   │   │   └── v1/
│   │   │       ├── __init__.py
│   │   │       ├── router.py
│   │   │       └── endpoints/
│   │   │           ├── __init__.py
│   │   │           ├── upload.py
│   │   │           ├── analysis.py
│   │   │           └── health.py
│   │   │
│   │   ├── core/                   # Core functionality
│   │   │   ├── __init__.py
│   │   │   ├── security.py
│   │   │   ├── logging.py
│   │   │   └── exceptions.py
│   │   │
│   │   ├── models/                 # Pydantic models
│   │   │   ├── __init__.py
│   │   │   ├── schemas.py          # Request/Response schemas
│   │   │   └── database.py         # SQLAlchemy models (optionnel)
│   │   │
│   │   ├── services/               # Business logic
│   │   │   ├── __init__.py
│   │   │   ├── pdf_extractor.py    # Extraction PDF
│   │   │   ├── nlp_processor.py    # Traitement NLP (spaCy)
│   │   │   ├── semantic_matcher.py # Matching sémantique (ST)
│   │   │   ├── llm_suggestions.py  # Appels LLM (Claude/GPT)
│   │   │   ├── scoring.py          # Calcul des scores
│   │   │   └── visualization.py    # Préparation données viz
│   │   │
│   │   ├── utils/                  # Utilitaires
│   │   │   ├── __init__.py
│   │   │   ├── file_handler.py
│   │   │   ├── text_cleaner.py
│   │   │   └── validators.py
│   │   │
│   │   └── db/                     # Database (optionnel)
│   │       ├── __init__.py
│   │       ├── session.py
│   │       └── repositories/
│   │
│   ├── uploads/                    # Stockage temporaire PDF
│   │
│   ├── models_cache/               # Cache des modèles ML
│   │
│   └── tests/                      # Tests unitaires
│       ├── __init__.py
│       ├── conftest.py
│       ├── test_pdf_extractor.py
│       ├── test_nlp_processor.py
│       ├── test_semantic_matcher.py
│       └── test_api.py
│
├── nginx/                          # Configuration Nginx
│   ├── Dockerfile
│   └── nginx.conf
│
├── scripts/                        # Scripts utilitaires
│   ├── download_models.py          # Téléchargement modèles spaCy
│   ├── seed_db.py                  # Seed database
│   └── test_integration.sh         # Tests d'intégration
│
└── docs/                           # Documentation
    ├── API.md                      # Documentation API
    ├── DEPLOYMENT.md               # Guide déploiement
    └── CONTRIBUTING.md             # Guide contribution
```

---

## 🔧 Stack Technique

### Frontend

| Technologie | Version | Utilisation |
|-------------|---------|-------------|
| React | 18.3+ | Framework UI |
| TypeScript | 5.0+ | Type safety |
| Vite | 5.0+ | Build tool & dev server |
| Tailwind CSS | 3.4+ | Styling |
| shadcn/ui | Latest | Composants UI |
| Chart.js | 4.4+ | Graphiques |
| react-chartjs-2 | 5.2+ | Wrapper React pour Chart.js |
| react-dropzone | 14.2+ | Upload de fichiers |
| Axios | 1.6+ | HTTP client |
| Zustand | 4.5+ | State management |
| React Router | 6.20+ | Routing |
| date-fns | 3.0+ | Date manipulation |

### Backend

| Technologie | Version | Utilisation |
|-------------|---------|-------------|
| Python | 3.11+ | Langage backend |
| FastAPI | 0.109+ | Framework web |
| Uvicorn | 0.27+ | ASGI server |
| Pydantic | 2.5+ | Validation données |
| PyPDF2 | 3.0+ | Extraction PDF |
| pdfplumber | 0.10+ | Extraction PDF avancée |
| spaCy | 3.7+ | NLP processing |
| sentence-transformers | 2.3+ | Embeddings sémantiques |
| scikit-learn | 1.4+ | Calculs ML |
| NLTK | 3.8+ | Text preprocessing |
| anthropic | 0.18+ | Claude API |
| openai | 1.10+ | OpenAI API (alternative) |
| SQLAlchemy | 2.0+ | ORM (optionnel) |
| Redis | 5.0+ | Caching |
| python-multipart | 0.0.6+ | Upload de fichiers |
| python-dotenv | 1.0+ | Variables d'environnement |
| pytest | 8.0+ | Testing |

### Infrastructure

| Technologie | Version | Utilisation |
|-------------|---------|-------------|
| Docker | 24.0+ | Containerization |
| Docker Compose | 2.24+ | Orchestration |
| Nginx | 1.25+ | Reverse proxy |
| PostgreSQL | 15+ | Base de données |
| Redis | 7+ | Cache & queues |

### Modèles NLP/ML

| Modèle | Utilisation |
|--------|-------------|
| `fr_core_news_lg` | spaCy français (NER, POS tagging) |
| `en_core_web_lg` | spaCy anglais |
| `paraphrase-multilingual-mpnet-base-v2` | Embeddings multilingues |
| `all-MiniLM-L6-v2` | Embeddings légers (alternative) |

---

## 🔄 Pipeline de Traitement

### Étape 1 : Extraction du Texte (PDF → Text)

```python
# services/pdf_extractor.py

def extract_text_from_pdf(pdf_file: UploadFile) -> dict:
    """
    Extrait le texte d'un CV PDF
    
    Returns:
        {
            'text': str,           # Texte brut
            'metadata': dict,      # Infos PDF
            'sections': dict,      # Sections détectées
            'pages': int           # Nombre de pages
        }
    """
    - Utilise PyPDF2 pour extraction basique
    - Fallback sur pdfplumber pour PDF complexes
    - Détection automatique de l'encodage
    - Nettoyage du texte (whitespaces, caractères spéciaux)
    - Détection des sections (Expérience, Formation, Compétences)
```

### Étape 2 : Traitement NLP (Text → Entities)

```python
# services/nlp_processor.py

def process_cv_text(text: str, language: str = 'fr') -> dict:
    """
    Analyse NLP du CV
    
    Returns:
        {
            'entities': {
                'skills': List[str],
                'experiences': List[dict],
                'education': List[dict],
                'languages': List[str],
                'certifications': List[str]
            },
            'metadata': {
                'name': str,
                'email': str,
                'phone': str,
                'location': str
            }
        }
    """
    - Tokenization avec spaCy
    - Named Entity Recognition (NER)
    - POS Tagging
    - Dependency Parsing
    - Custom patterns pour compétences techniques
    - Extraction d'entités personnalisées (technologies, frameworks)
```

### Étape 3 : Analyse de l'Offre d'Emploi

```python
# services/nlp_processor.py

def process_job_description(text: str) -> dict:
    """
    Analyse de l'offre d'emploi
    
    Returns:
        {
            'required_skills': List[str],
            'preferred_skills': List[str],
            'experience_required': dict,
            'education_required': str,
            'job_type': str,
            'keywords': List[str]
        }
    """
    - Extraction des compétences requises
    - Détection des mots-clés ATS
    - Identification des exigences obligatoires vs souhaitées
    - Extraction du niveau d'expérience requis
```

### Étape 4 : Matching Sémantique

```python
# services/semantic_matcher.py

def calculate_semantic_match(cv_data: dict, job_data: dict) -> dict:
    """
    Calcule la similarité sémantique
    
    Process:
        1. Génération d'embeddings (sentence-transformers)
        2. Calcul de similarité cosine
        3. Matching par catégorie (skills, experience, etc.)
        4. Score global et sous-scores
    
    Returns:
        {
            'overall_score': float,        # 0-100
            'category_scores': {
                'technical_skills': float,
                'soft_skills': float,
                'experience': float,
                'education': float,
                'keywords': float
            },
            'matched_items': List[dict],
            'missing_items': List[dict]
        }
    """
```

### Étape 5 : Génération de Suggestions (LLM)

```python
# services/llm_suggestions.py

async def generate_suggestions(
    cv_data: dict,
    job_data: dict,
    matching_results: dict
) -> List[dict]:
    """
    Génère des suggestions d'amélioration via Claude/GPT
    
    Returns:
        [
            {
                'category': 'skills',
                'priority': 'high',
                'title': 'Ajouter Python',
                'description': 'Detailed suggestion...',
                'impact': 'Augmente score de 15%',
                'implementation': 'Concrete steps...'
            },
            ...
        ]
    """
    - Prompt engineering optimisé
    - Suggestions actionnables et concrètes
    - Priorisation (high, medium, low)
    - Estimation de l'impact
```

### Étape 6 : Préparation des Visualisations

```python
# services/visualization.py

def prepare_visualization_data(analysis: dict) -> dict:
    """
    Prépare les données pour Chart.js
    
    Returns:
        {
            'radar_chart': {
                'labels': List[str],
                'datasets': [
                    {
                        'label': 'CV',
                        'data': List[float]
                    },
                    {
                        'label': 'Job Required',
                        'data': List[float]
                    }
                ]
            },
            'score_gauge': {...},
            'category_bars': {...},
            'keywords_cloud': {...}
        }
    """
```

---

## 📊 Modèles de Données

### Request/Response Schemas

```python
# models/schemas.py

from pydantic import BaseModel, Field, validator
from typing import List, Dict, Optional
from datetime import datetime
from enum import Enum

# ==================== ENUMS ====================

class SkillCategory(str, Enum):
    TECHNICAL = "technical"
    SOFT_SKILL = "soft_skill"
    LANGUAGE = "language"
    TOOL = "tool"
    FRAMEWORK = "framework"

class Priority(str, Enum):
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"

# ==================== SKILL MODELS ====================

class Skill(BaseModel):
    name: str
    category: SkillCategory
    proficiency: Optional[float] = Field(None, ge=0, le=100)
    mentioned_in_cv: bool = False
    mentioned_in_job: bool = False
    relevance_score: Optional[float] = Field(None, ge=0, le=1)

class SkillMatch(BaseModel):
    skill: Skill
    match_score: float = Field(..., ge=0, le=100)
    is_exact_match: bool
    similar_terms: List[str] = []

# ==================== EXPERIENCE MODELS ====================

class Experience(BaseModel):
    title: str
    company: Optional[str] = None
    duration_months: Optional[int] = None
    description: Optional[str] = None
    skills_used: List[str] = []
    start_date: Optional[str] = None
    end_date: Optional[str] = None

class Education(BaseModel):
    degree: str
    institution: Optional[str] = None
    field: Optional[str] = None
    year: Optional[int] = None

# ==================== SCORING MODELS ====================

class CategoryScore(BaseModel):
    technical_skills: float = Field(..., ge=0, le=100)
    soft_skills: float = Field(..., ge=0, le=100)
    experience: float = Field(..., ge=0, le=100)
    education: float = Field(..., ge=0, le=100)
    keywords_ats: float = Field(..., ge=0, le=100)

class MatchingScore(BaseModel):
    overall_score: float = Field(..., ge=0, le=100)
    category_scores: CategoryScore
    confidence_level: float = Field(..., ge=0, le=1)
    
    @property
    def grade(self) -> str:
        if self.overall_score >= 80:
            return "Excellent Match"
        elif self.overall_score >= 60:
            return "Good Match"
        elif self.overall_score >= 40:
            return "Moderate Match"
        else:
            return "Low Match"

# ==================== ANALYSIS MODELS ====================

class StrengthWeakness(BaseModel):
    title: str
    description: str
    category: str
    impact: str  # "positive" or "negative"

class Suggestion(BaseModel):
    id: str
    category: SkillCategory
    priority: Priority
    title: str
    description: str
    impact_estimation: str
    implementation_steps: List[str]
    before_example: Optional[str] = None
    after_example: Optional[str] = None

# ==================== VISUALIZATION MODELS ====================

class RadarChartData(BaseModel):
    labels: List[str]
    cv_data: List[float]
    job_data: List[float]
    max_value: float = 100

class ChartDataset(BaseModel):
    label: str
    data: List[float]
    backgroundColor: Optional[str] = None
    borderColor: Optional[str] = None

# ==================== MAIN ANALYSIS ====================

class CVAnalysis(BaseModel):
    cv_text: str
    extracted_skills: List[Skill]
    experiences: List[Experience]
    education: List[Education]
    languages: List[str]
    certifications: List[str]
    metadata: Dict[str, str]

class JobAnalysis(BaseModel):
    job_text: str
    required_skills: List[Skill]
    preferred_skills: List[Skill]
    experience_required: Dict[str, any]
    education_required: Optional[str] = None
    keywords: List[str]

class AnalysisResult(BaseModel):
    id: str
    created_at: datetime
    cv_analysis: CVAnalysis
    job_analysis: JobAnalysis
    matching_score: MatchingScore
    skill_matches: List[SkillMatch]
    strengths: List[StrengthWeakness]
    weaknesses: List[StrengthWeakness]
    suggestions: List[Suggestion]
    radar_chart_data: RadarChartData
    processing_time_ms: int

# ==================== API REQUEST/RESPONSE ====================

class AnalyzeRequest(BaseModel):
    job_description: str = Field(..., min_length=50, max_length=10000)
    language: str = Field(default="fr", pattern="^(fr|en)$")

class AnalyzeResponse(BaseModel):
    success: bool
    analysis: AnalysisResult
    message: Optional[str] = None

class ErrorResponse(BaseModel):
    success: bool = False
    error: str
    details: Optional[Dict] = None
```

---

## 🔌 API Endpoints

### Base URL
```
Development: http://localhost:8000
Production: https://api.cvanalyzer.com
```

### Endpoints

#### 1. Health Check
```http
GET /api/health
```

**Response:**
```json
{
  "status": "healthy",
  "version": "1.0.0",
  "timestamp": "2024-01-15T10:30:00Z",
  "services": {
    "database": "connected",
    "redis": "connected",
    "nlp_models": "loaded"
  }
}
```

#### 2. Upload CV
```http
POST /api/v1/upload
Content-Type: multipart/form-data
```

**Request:**
```
file: <PDF file>
```

**Response:**
```json
{
  "success": true,
  "file_id": "uuid-here",
  "filename": "cv.pdf",
  "size_bytes": 245678,
  "pages": 2,
  "text_preview": "First 200 chars..."
}
```

#### 3. Analyze CV vs Job
```http
POST /api/v1/analyze
Content-Type: multipart/form-data
```

**Request:**
```
file: <PDF file>
job_description: <text>
language: "fr" | "en"  (optional, default: "fr")
```

**Response:**
```json
{
  "success": true,
  "analysis": {
    "id": "analysis-uuid",
    "created_at": "2024-01-15T10:30:00Z",
    "matching_score": {
      "overall_score": 78.5,
      "category_scores": {
        "technical_skills": 85.0,
        "soft_skills": 70.0,
        "experience": 80.0,
        "education": 75.0,
        "keywords_ats": 82.0
      },
      "confidence_level": 0.92,
      "grade": "Good Match"
    },
    "cv_analysis": {
      "extracted_skills": [
        {
          "name": "Python",
          "category": "technical",
          "proficiency": 85,
          "mentioned_in_cv": true,
          "mentioned_in_job": true,
          "relevance_score": 0.95
        }
      ],
      "experiences": [...],
      "education": [...],
      "languages": ["Français", "Anglais"],
      "certifications": ["AWS Certified"],
      "metadata": {
        "name": "John Doe",
        "email": "john@example.com"
      }
    },
    "job_analysis": {
      "required_skills": [...],
      "preferred_skills": [...],
      "experience_required": {
        "years": 3,
        "level": "mid"
      },
      "keywords": ["Python", "FastAPI", "Docker"]
    },
    "skill_matches": [
      {
        "skill": {...},
        "match_score": 95.0,
        "is_exact_match": true,
        "similar_terms": ["Python3", "Python 3"]
      }
    ],
    "strengths": [
      {
        "title": "Strong Python Experience",
        "description": "5 years of Python development...",
        "category": "technical_skills",
        "impact": "positive"
      }
    ],
    "weaknesses": [
      {
        "title": "Missing Kubernetes Experience",
        "description": "Job requires Kubernetes...",
        "category": "technical_skills",
        "impact": "negative"
      }
    ],
    "suggestions": [
      {
        "id": "sug-1",
        "category": "technical",
        "priority": "high",
        "title": "Add Kubernetes to your CV",
        "description": "The job requires Kubernetes experience...",
        "impact_estimation": "Could increase match score by ~12%",
        "implementation_steps": [
          "Complete a Kubernetes certification",
          "Add a project using K8s to your CV",
          "Highlight container orchestration skills"
        ],
        "before_example": "Managed Docker containers",
        "after_example": "Orchestrated microservices using Kubernetes (K8s) with 99.9% uptime"
      }
    ],
    "radar_chart_data": {
      "labels": [
        "Technical Skills",
        "Soft Skills",
        "Experience",
        "Education",
        "ATS Keywords"
      ],
      "cv_data": [85, 70, 80, 75, 82],
      "job_data": [90, 75, 85, 70, 85],
      "max_value": 100
    },
    "processing_time_ms": 3450
  }
}
```

#### 4. Get Previous Analyses (optionnel)
```http
GET /api/v1/analyses?limit=10&offset=0
```

**Response:**
```json
{
  "success": true,
  "total": 25,
  "analyses": [
    {
      "id": "uuid",
      "created_at": "2024-01-15T10:30:00Z",
      "overall_score": 78.5,
      "job_title": "Backend Developer"
    }
  ]
}
```

---

## 🎨 Composants Frontend

### 1. CVUploader Component

```typescript
// components/upload/CVUploader.tsx

interface CVUploaderProps {
  onFileSelect: (file: File) => void;
  isUploading: boolean;
}

export const CVUploader: React.FC<CVUploaderProps> = ({
  onFileSelect,
  isUploading
}) => {
  // Drag & drop avec react-dropzone
  // Validation: PDF uniquement, max 10MB
  // Preview du fichier sélectionné
  // Progress bar pendant l'upload
};
```

### 2. JobDescriptionInput Component

```typescript
// components/upload/JobDescriptionInput.tsx

interface JobDescriptionInputProps {
  value: string;
  onChange: (value: string) => void;
  maxLength?: number;
}

export const JobDescriptionInput: React.FC<JobDescriptionInputProps> = ({
  value,
  onChange,
  maxLength = 10000
}) => {
  // Textarea avec compteur de caractères
  // Validation: min 50 chars
  // Auto-resize
  // Paste detection pour offres copiées
};
```

### 3. SkillsRadarChart Component

```typescript
// components/analysis/SkillsRadarChart.tsx

import { Radar } from 'react-chartjs-2';

interface SkillsRadarChartProps {
  data: RadarChartData;
}

export const SkillsRadarChart: React.FC<SkillsRadarChartProps> = ({ data }) => {
  const chartData = {
    labels: data.labels,
    datasets: [
      {
        label: 'Votre CV',
        data: data.cv_data,
        backgroundColor: 'rgba(59, 130, 246, 0.2)',
        borderColor: 'rgb(59, 130, 246)',
        borderWidth: 2,
      },
      {
        label: 'Requis par l\'offre',
        data: data.job_data,
        backgroundColor: 'rgba(239, 68, 68, 0.2)',
        borderColor: 'rgb(239, 68, 68)',
        borderWidth: 2,
      }
    ]
  };

  const options = {
    scales: {
      r: {
        beginAtZero: true,
        max: data.max_value,
        ticks: { stepSize: 20 }
      }
    },
    plugins: {
      legend: { position: 'top' as const },
      tooltip: { enabled: true }
    }
  };

  return <Radar data={chartData} options={options} />;
};
```

### 4. MatchingScore Component

```typescript
// components/analysis/MatchingScore.tsx

interface MatchingScoreProps {
  score: MatchingScore;
}

export const MatchingScore: React.FC<MatchingScoreProps> = ({ score }) => {
  return (
    <div className="space-y-6">
      {/* Gauge principal */}
      <ScoreGauge 
        value={score.overall_score} 
        label={score.grade}
      />
      
      {/* Breakdown par catégorie */}
      <CategoryBreakdown scores={score.category_scores} />
      
      {/* Niveau de confiance */}
      <ConfidenceIndicator level={score.confidence_level} />
    </div>
  );
};
```

### 5. ImprovementSuggestions Component

```typescript
// components/results/ImprovementSuggestions.tsx

interface ImprovementSuggestionsProps {
  suggestions: Suggestion[];
}

export const ImprovementSuggestions: React.FC<ImprovementSuggestionsProps> = ({
  suggestions
}) => {
  // Groupement par priorité (high, medium, low)
  // Cartes expandables pour chaque suggestion
  // Before/After examples
  // Implementation steps en checklist
  // Estimation de l'impact sur le score
};
```

---

## ⚙️ Services Backend

### 1. PDF Extractor Service

```python
# services/pdf_extractor.py

import PyPDF2
import pdfplumber
import re
from typing import Dict, List

class PDFExtractor:
    
    @staticmethod
    def extract_text(file_path: str) -> Dict:
        """
        Extrait le texte d'un PDF avec fallback
        """
        try:
            # Tentative avec PyPDF2 (rapide)
            text = PDFExtractor._extract_with_pypdf2(file_path)
            
            if PDFExtractor._is_valid_extraction(text):
                return {
                    'text': text,
                    'method': 'pypdf2',
                    'success': True
                }
            
            # Fallback sur pdfplumber (plus robuste)
            text = PDFExtractor._extract_with_pdfplumber(file_path)
            return {
                'text': text,
                'method': 'pdfplumber',
                'success': True
            }
            
        except Exception as e:
            return {
                'text': '',
                'method': None,
                'success': False,
                'error': str(e)
            }
    
    @staticmethod
    def _extract_with_pypdf2(file_path: str) -> str:
        with open(file_path, 'rb') as file:
            reader = PyPDF2.PdfReader(file)
            text = ''
            for page in reader.pages:
                text += page.extract_text()
        return PDFExtractor._clean_text(text)
    
    @staticmethod
    def _extract_with_pdfplumber(file_path: str) -> str:
        with pdfplumber.open(file_path) as pdf:
            text = ''
            for page in pdf.pages:
                text += page.extract_text()
        return PDFExtractor._clean_text(text)
    
    @staticmethod
    def _clean_text(text: str) -> str:
        # Supprime whitespaces multiples
        text = re.sub(r'\s+', ' ', text)
        # Supprime caractères spéciaux problématiques
        text = re.sub(r'[^\w\s\-.,;:!?()/]', '', text)
        return text.strip()
    
    @staticmethod
    def _is_valid_extraction(text: str) -> bool:
        # Vérification basique de qualité
        return len(text) > 100 and len(text.split()) > 20
    
    @staticmethod
    def detect_sections(text: str) -> Dict[str, str]:
        """
        Détecte les sections principales du CV
        """
        sections = {}
        
        patterns = {
            'experience': r'(exp[eé]rience professionnelle|professional experience)',
            'education': r'(formation|education|diplômes)',
            'skills': r'(comp[eé]tences|skills|technical skills)',
            'languages': r'(langues|languages)',
        }
        
        for section, pattern in patterns.items():
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                start = match.start()
                # Extraire jusqu'à la prochaine section
                sections[section] = text[start:start+1000]
        
        return sections
```

### 2. NLP Processor Service

```python
# services/nlp_processor.py

import spacy
from typing import List, Dict
import re

class NLPProcessor:
    
    def __init__(self, language: str = 'fr'):
        self.language = language
        # Charger le modèle spaCy approprié
        if language == 'fr':
            self.nlp = spacy.load('fr_core_news_lg')
        else:
            self.nlp = spacy.load('en_core_web_lg')
        
        # Skills techniques communs
        self.tech_skills = self._load_tech_skills()
    
    def process_cv(self, text: str) -> Dict:
        """
        Traite le texte du CV avec spaCy
        """
        doc = self.nlp(text)
        
        return {
            'entities': self._extract_entities(doc),
            'skills': self._extract_skills(doc, text),
            'metadata': self._extract_metadata(text),
            'tokens': len(doc),
            'sentences': len(list(doc.sents))
        }
    
    def _extract_entities(self, doc) -> Dict:
        """
        Extraction d'entités nommées
        """
        entities = {
            'persons': [],
            'organizations': [],
            'locations': [],
            'dates': []
        }
        
        for ent in doc.ents:
            if ent.label_ == 'PER' or ent.label_ == 'PERSON':
                entities['persons'].append(ent.text)
            elif ent.label_ == 'ORG':
                entities['organizations'].append(ent.text)
            elif ent.label_ in ['LOC', 'GPE']:
                entities['locations'].append(ent.text)
            elif ent.label_ == 'DATE':
                entities['dates'].append(ent.text)
        
        return entities
    
    def _extract_skills(self, doc, text: str) -> List[Dict]:
        """
        Extraction des compétences techniques
        """
        skills = []
        text_lower = text.lower()
        
        # Recherche de skills prédéfinis
        for skill_category, skill_list in self.tech_skills.items():
            for skill in skill_list:
                if skill.lower() in text_lower:
                    skills.append({
                        'name': skill,
                        'category': skill_category,
                        'mentioned': True
                    })
        
        # Extraction via patterns
        # Ex: "3 ans d'expérience en Python"
        experience_pattern = r'(\d+)\s*(ans?|years?)\s*(d[\'e]|of)?\s*(expérience|experience)\s*(en|in|with)\s+(\w+)'
        matches = re.finditer(experience_pattern, text_lower)
        
        for match in matches:
            skill_name = match.group(6)
            years = int(match.group(1))
            skills.append({
                'name': skill_name,
                'category': 'experience',
                'years': years
            })
        
        return skills
    
    def _extract_metadata(self, text: str) -> Dict:
        """
        Extraction métadonnées (email, téléphone, etc.)
        """
        metadata = {}
        
        # Email
        email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        email_match = re.search(email_pattern, text)
        if email_match:
            metadata['email'] = email_match.group()
        
        # Téléphone (FR format)
        phone_pattern = r'(?:(?:\+|00)33|0)\s*[1-9](?:[\s.-]*\d{2}){4}'
        phone_match = re.search(phone_pattern, text)
        if phone_match:
            metadata['phone'] = phone_match.group()
        
        # LinkedIn
        linkedin_pattern = r'linkedin\.com/in/[\w-]+'
        linkedin_match = re.search(linkedin_pattern, text, re.IGNORECASE)
        if linkedin_match:
            metadata['linkedin'] = linkedin_match.group()
        
        return metadata
    
    def _load_tech_skills(self) -> Dict[str, List[str]]:
        """
        Charge une base de compétences techniques
        """
        return {
            'languages': [
                'Python', 'JavaScript', 'TypeScript', 'Java', 'C++', 'C#', 
                'Go', 'Rust', 'PHP', 'Ruby', 'Swift', 'Kotlin', 'Scala'
            ],
            'frameworks': [
                'React', 'Vue', 'Angular', 'Django', 'Flask', 'FastAPI',
                'Express', 'NestJS', 'Spring', 'Laravel', 'Rails'
            ],
            'databases': [
                'PostgreSQL', 'MySQL', 'MongoDB', 'Redis', 'Elasticsearch',
                'Oracle', 'SQL Server', 'Cassandra', 'DynamoDB'
            ],
            'devops': [
                'Docker', 'Kubernetes', 'Jenkins', 'GitLab CI', 'GitHub Actions',
                'Terraform', 'Ansible', 'AWS', 'Azure', 'GCP'
            ],
            'tools': [
                'Git', 'Jira', 'Confluence', 'Slack', 'VS Code', 'IntelliJ',
                'Postman', 'Figma', 'Tableau', 'Power BI'
            ]
        }
```

### 3. Semantic Matcher Service

```python
# services/semantic_matcher.py

from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
from typing import List, Dict

class SemanticMatcher:
    
    def __init__(self, model_name: str = 'paraphrase-multilingual-mpnet-base-v2'):
        self.model = SentenceTransformer(model_name)
    
    def calculate_match_score(
        self,
        cv_skills: List[str],
        job_skills: List[str]
    ) -> Dict:
        """
        Calcule le score de matching sémantique
        """
        # Générer embeddings
        cv_embeddings = self.model.encode(cv_skills)
        job_embeddings = self.model.encode(job_skills)
        
        # Matrice de similarité
        similarity_matrix = cosine_similarity(cv_embeddings, job_embeddings)
        
        # Analyser les matches
        matches = []
        for i, cv_skill in enumerate(cv_skills):
            for j, job_skill in enumerate(job_skills):
                score = similarity_matrix[i][j]
                if score > 0.7:  # Seuil de similarité
                    matches.append({
                        'cv_skill': cv_skill,
                        'job_skill': job_skill,
                        'similarity': float(score),
                        'is_exact': score > 0.95
                    })
        
        # Calculer score global
        overall_score = self._calculate_overall_score(similarity_matrix)
        
        return {
            'overall_score': overall_score,
            'matches': matches,
            'coverage': len(matches) / len(job_skills) * 100
        }
    
    def _calculate_overall_score(self, similarity_matrix: np.ndarray) -> float:
        """
        Calcule un score global de matching
        """
        # Pour chaque compétence requise, prendre le meilleur match
        best_matches = np.max(similarity_matrix, axis=0)
        
        # Score = moyenne des meilleurs matches
        score = np.mean(best_matches) * 100
        
        return float(score)
    
    def find_similar_skills(
        self,
        skill: str,
        candidate_skills: List[str],
        threshold: float = 0.7
    ) -> List[Dict]:
        """
        Trouve les compétences similaires
        """
        skill_embedding = self.model.encode([skill])
        candidate_embeddings = self.model.encode(candidate_skills)
        
        similarities = cosine_similarity(skill_embedding, candidate_embeddings)[0]
        
        similar = []
        for i, candidate in enumerate(candidate_skills):
            if similarities[i] > threshold:
                similar.append({
                    'skill': candidate,
                    'similarity': float(similarities[i])
                })
        
        return sorted(similar, key=lambda x: x['similarity'], reverse=True)
```

### 4. LLM Suggestions Service

```python
# services/llm_suggestions.py

from anthropic import Anthropic
from typing import List, Dict
import json

class LLMSuggestionsService:
    
    def __init__(self, api_key: str):
        self.client = Anthropic(api_key=api_key)
    
    async def generate_suggestions(
        self,
        cv_analysis: Dict,
        job_analysis: Dict,
        matching_results: Dict
    ) -> List[Dict]:
        """
        Génère des suggestions d'amélioration via Claude
        """
        prompt = self._build_prompt(cv_analysis, job_analysis, matching_results)
        
        response = self.client.messages.create(
            model="claude-sonnet-4-20250514",
            max_tokens=2000,
            messages=[{
                "role": "user",
                "content": prompt
            }]
        )
        
        # Parser la réponse
        suggestions_text = response.content[0].text
        suggestions = self._parse_suggestions(suggestions_text)
        
        return suggestions
    
    def _build_prompt(self, cv_analysis, job_analysis, matching_results) -> str:
        """
        Construit le prompt pour Claude
        """
        return f"""
Tu es un expert en recrutement et optimisation de CV. Analyse le CV suivant par rapport à l'offre d'emploi et fournis des suggestions concrètes d'amélioration.

CV SKILLS:
{json.dumps(cv_analysis['skills'], indent=2)}

JOB REQUIREMENTS:
{json.dumps(job_analysis['required_skills'], indent=2)}

MATCHING RESULTS:
- Score global: {matching_results['overall_score']}/100
- Compétences manquantes: {len(matching_results.get('missing_skills', []))}
- Couverture: {matching_results.get('coverage', 0)}%

TÂCHE:
Génère 5-7 suggestions d'amélioration CONCRÈTES et ACTIONNABLES pour améliorer ce CV.

Pour chaque suggestion, fournis:
1. Un titre court
2. La catégorie (technical_skills, soft_skills, experience, education, formatting)
3. La priorité (high, medium, low)
4. Une description détaillée
5. Des étapes d'implémentation concrètes
6. Un exemple "avant/après" si applicable
7. Une estimation de l'impact sur le score

Format de réponse: JSON array de suggestions.

IMPORTANT:
- Sois SPÉCIFIQUE et ACTIONNABLE
- Pas de généralités type "améliorez vos compétences"
- Donne des exemples concrets de formulations
- Priorise les suggestions à fort impact
"""
    
    def _parse_suggestions(self, text: str) -> List[Dict]:
        """
        Parse la réponse de Claude en suggestions structurées
        """
        try:
            # Essayer de parser comme JSON
            suggestions = json.loads(text)
            return suggestions
        except json.JSONDecodeError:
            # Fallback: extraction manuelle
            return self._manual_parse(text)
    
    def _manual_parse(self, text: str) -> List[Dict]:
        """
        Parse manuel si JSON échoue
        """
        # Implémenter parsing avec regex si nécessaire
        suggestions = []
        # ... logique de parsing ...
        return suggestions
```

---

## 🐳 Configuration Docker

### Dockerfile - Frontend

```dockerfile
# frontend/Dockerfile

FROM node:20-alpine AS builder

WORKDIR /app

# Copier package files
COPY package*.json ./

# Install dependencies
RUN npm ci

# Copier source code
COPY . .

# Build l'application
RUN npm run build

# Production stage
FROM nginx:alpine

# Copier build
COPY --from=builder /app/dist /usr/share/nginx/html

# Copier config nginx custom (optionnel)
COPY nginx.conf /etc/nginx/conf.d/default.conf

EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]
```

### Dockerfile - Backend

```dockerfile
# backend/Dockerfile

FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copier requirements
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Télécharger modèles spaCy
RUN python -m spacy download fr_core_news_lg
RUN python -m spacy download en_core_web_lg

# Copier code source
COPY ./app ./app

# Créer dossiers nécessaires
RUN mkdir -p /app/uploads /app/models_cache

# Exposer port
EXPOSE 8000

# Health check
HEALTHCHECK --interval=30s --timeout=3s --start-period=40s --retries=3 \
  CMD curl -f http://localhost:8000/api/health || exit 1

# Run avec uvicorn
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--workers", "2"]
```

### docker-compose.yml (complet)

```yaml
version: '3.8'

services:
  # ==================== FRONTEND ====================
  frontend:
    build:
      context: ./frontend
      dockerfile: Dockerfile
    container_name: cvanalyzer_frontend
    ports:
      - "3000:80"
    environment:
      - VITE_API_URL=http://localhost:8000
      - VITE_APP_NAME=CV Analyzer
    depends_on:
      - backend
    networks:
      - cvanalyzer_network
    restart: unless-stopped

  # ==================== BACKEND ====================
  backend:
    build:
      context: ./backend
      dockerfile: Dockerfile
    container_name: cvanalyzer_backend
    ports:
      - "8000:8000"
    environment:
      # Database
      - DATABASE_URL=postgresql://cvuser:cvpassword@db:5432/cvanalyzer
      # Redis
      - REDIS_URL=redis://redis:6379/0
      # LLM APIs
      - ANTHROPIC_API_KEY=${ANTHROPIC_API_KEY}
      - OPENAI_API_KEY=${OPENAI_API_KEY}
      # App config
      - DEBUG=false
      - MAX_UPLOAD_SIZE=10485760  # 10MB
      - CORS_ORIGINS=http://localhost:3000,http://localhost:80
    volumes:
      - ./backend/app:/app/app
      - uploaded_files:/app/uploads
      - models_cache:/app/models_cache
    depends_on:
      db:
        condition: service_healthy
      redis:
        condition: service_started
    networks:
      - cvanalyzer_network
    restart: unless-stopped

  # ==================== DATABASE ====================
  db:
    image: postgres:15-alpine
    container_name: cvanalyzer_db
    environment:
      - POSTGRES_USER=cvuser
      - POSTGRES_PASSWORD=cvpassword
      - POSTGRES_DB=cvanalyzer
    volumes:
      - postgres_data:/var/lib/postgresql/data
      - ./scripts/init.sql:/docker-entrypoint-initdb.d/init.sql
    ports:
      - "5432:5432"
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U cvuser -d cvanalyzer"]
      interval: 10s
      timeout: 5s
      retries: 5
    networks:
      - cvanalyzer_network
    restart: unless-stopped

  # ==================== REDIS ====================
  redis:
    image: redis:7-alpine
    container_name: cvanalyzer_redis
    command: redis-server --appendonly yes
    volumes:
      - redis_data:/data
    ports:
      - "6379:6379"
    healthcheck:
      test: ["CMD", "redis-cli", "ping"]
      interval: 10s
      timeout: 3s
      retries: 5
    networks:
      - cvanalyzer_network
    restart: unless-stopped

  # ==================== NGINX (optional) ====================
  nginx:
    build:
      context: ./nginx
      dockerfile: Dockerfile
    container_name: cvanalyzer_nginx
    ports:
      - "80:80"
      - "443:443"
    depends_on:
      - frontend
      - backend
    volumes:
      - ./nginx/nginx.conf:/etc/nginx/nginx.conf:ro
      - ./nginx/ssl:/etc/nginx/ssl:ro
    networks:
      - cvanalyzer_network
    restart: unless-stopped

# ==================== VOLUMES ====================
volumes:
  postgres_data:
    driver: local
  redis_data:
    driver: local
  uploaded_files:
    driver: local
  models_cache:
    driver: local

# ==================== NETWORKS ====================
networks:
  cvanalyzer_network:
    driver: bridge
```

### .env.example

```bash
# ==================== API KEYS ====================
ANTHROPIC_API_KEY=your_anthropic_key_here
OPENAI_API_KEY=your_openai_key_here

# ==================== DATABASE ====================
DATABASE_URL=postgresql://cvuser:cvpassword@localhost:5432/cvanalyzer
POSTGRES_USER=cvuser
POSTGRES_PASSWORD=cvpassword
POSTGRES_DB=cvanalyzer

# ==================== REDIS ====================
REDIS_URL=redis://localhost:6379/0

# ==================== APP CONFIG ====================
DEBUG=true
ENVIRONMENT=development
MAX_UPLOAD_SIZE=10485760
CORS_ORIGINS=http://localhost:3000,http://localhost:5173

# ==================== FRONTEND ====================
VITE_API_URL=http://localhost:8000
VITE_APP_NAME=CV Analyzer
```

---

## 🚀 Étapes d'Implémentation

### Phase 1: Setup Initial (Jour 1-2)

#### 1.1 Initialisation du Projet
```bash
# Créer structure de base
mkdir cv-analyzer-matching
cd cv-analyzer-matching

# Créer sous-dossiers
mkdir -p frontend backend nginx scripts docs

# Initialiser Git
git init
echo "node_modules/
__pycache__/
*.pyc
.env
uploads/
*.pdf
.DS_Store" > .gitignore

# Créer .env
cp .env.example .env
```

#### 1.2 Setup Frontend
```bash
cd frontend

# Créer projet Vite React TypeScript
npm create vite@latest . -- --template react-ts

# Installer dépendances
npm install axios react-router-dom zustand
npm install react-dropzone chart.js react-chartjs-2
npm install -D tailwindcss postcss autoprefixer
npm install @radix-ui/react-dropdown-menu @radix-ui/react-dialog
npm install lucide-react
npm install date-fns

# Setup Tailwind
npx tailwindcss init -p
```

**tailwind.config.js:**
```javascript
/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {},
  },
  plugins: [],
}
```

#### 1.3 Setup Backend
```bash
cd ../backend

# Créer environnement virtuel
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Créer requirements.txt
cat > requirements.txt << EOF
fastapi==0.109.0
uvicorn[standard]==0.27.0
pydantic==2.5.0
python-multipart==0.0.6
PyPDF2==3.0.1
pdfplumber==0.10.3
spacy==3.7.2
sentence-transformers==2.3.1
scikit-learn==1.4.0
anthropic==0.18.0
python-dotenv==1.0.0
redis==5.0.1
sqlalchemy==2.0.25
psycopg2-binary==2.9.9
pytest==8.0.0
httpx==0.26.0
EOF

# Installer
pip install -r requirements.txt

# Télécharger modèles spaCy
python -m spacy download fr_core_news_lg
python -m spacy download en_core_web_lg
```

#### 1.4 Configuration Docker
```bash
# Retour à la racine
cd ..

# Créer docker-compose.yml (voir section précédente)

# Créer Dockerfiles (voir section précédente)
```

### Phase 2: Backend Core (Jour 3-5)

#### 2.1 Structure Backend
```bash
cd backend
mkdir -p app/api/v1/endpoints app/services app/models app/core app/utils tests
touch app/__init__.py
touch app/main.py
touch app/config.py
```

#### 2.2 Configuration de Base (app/config.py)
```python
from pydantic_settings import BaseSettings
from functools import lru_cache

class Settings(BaseSettings):
    # App
    app_name: str = "CV Analyzer API"
    debug: bool = False
    
    # Database
    database_url: str
    
    # Redis
    redis_url: str
    
    # API Keys
    anthropic_api_key: str
    openai_api_key: str = ""
    
    # File Upload
    max_upload_size: int = 10 * 1024 * 1024  # 10MB
    allowed_extensions: list = [".pdf"]
    
    # CORS
    cors_origins: list = ["http://localhost:3000"]
    
    class Config:
        env_file = ".env"

@lru_cache()
def get_settings():
    return Settings()
```

#### 2.3 Main FastAPI App (app/main.py)
```python
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.config import get_settings
from app.api.v1.router import api_router

settings = get_settings()

app = FastAPI(
    title=settings.app_name,
    version="1.0.0",
    debug=settings.debug
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(api_router, prefix="/api/v1")

@app.get("/")
def root():
    return {"message": "CV Analyzer API", "version": "1.0.0"}

@app.get("/api/health")
def health_check():
    return {
        "status": "healthy",
        "version": "1.0.0"
    }
```

#### 2.4 Implémenter les Services
1. **PDF Extractor** (voir section Services Backend)
2. **NLP Processor** (voir section Services Backend)
3. **Semantic Matcher** (voir section Services Backend)
4. **LLM Suggestions** (voir section Services Backend)

#### 2.5 Créer les Endpoints
```python
# app/api/v1/endpoints/analysis.py

from fastapi import APIRouter, UploadFile, File, Form, HTTPException
from app.services.pdf_extractor import PDFExtractor
from app.services.nlp_processor import NLPProcessor
from app.services.semantic_matcher import SemanticMatcher
from app.services.llm_suggestions import LLMSuggestionsService
from app.models.schemas import AnalyzeResponse
import time

router = APIRouter()

@router.post("/analyze", response_model=AnalyzeResponse)
async def analyze_cv(
    file: UploadFile = File(...),
    job_description: str = Form(...),
    language: str = Form("fr")
):
    start_time = time.time()
    
    # Validation
    if not file.filename.endswith('.pdf'):
        raise HTTPException(400, "Only PDF files allowed")
    
    # 1. Extract PDF
    extractor = PDFExtractor()
    pdf_result = extractor.extract_text(file.file)
    
    if not pdf_result['success']:
        raise HTTPException(500, "Failed to extract PDF text")
    
    # 2. Process CV
    nlp_processor = NLPProcessor(language)
    cv_analysis = nlp_processor.process_cv(pdf_result['text'])
    
    # 3. Process Job Description
    job_analysis = nlp_processor.process_job_description(job_description)
    
    # 4. Semantic Matching
    matcher = SemanticMatcher()
    matching_results = matcher.calculate_match_score(
        cv_analysis['skills'],
        job_analysis['required_skills']
    )
    
    # 5. LLM Suggestions
    llm_service = LLMSuggestionsService(api_key=settings.anthropic_api_key)
    suggestions = await llm_service.generate_suggestions(
        cv_analysis,
        job_analysis,
        matching_results
    )
    
    # 6. Build Response
    processing_time = int((time.time() - start_time) * 1000)
    
    return AnalyzeResponse(
        success=True,
        analysis={
            'matching_score': matching_results,
            'cv_analysis': cv_analysis,
            'job_analysis': job_analysis,
            'suggestions': suggestions,
            'processing_time_ms': processing_time
        }
    )
```

### Phase 3: Frontend Development (Jour 6-9)

#### 3.1 Configuration API Client
```typescript
// src/services/api.ts

import axios from 'axios';

const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';

export const api = axios.create({
  baseURL: API_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

export const analyzeCV = async (file: File, jobDescription: string) => {
  const formData = new FormData();
  formData.append('file', file);
  formData.append('job_description', jobDescription);
  formData.append('language', 'fr');

  const response = await api.post('/api/v1/analyze', formData, {
    headers: {
      'Content-Type': 'multipart/form-data',
    },
  });

  return response.data;
};
```

#### 3.2 Créer les Composants Principaux
1. **CVUploader** - Upload de CV avec drag & drop
2. **JobDescriptionInput** - Zone de texte pour l'offre
3. **MatchingScore** - Affichage du score global
4. **SkillsRadarChart** - Radar chart des compétences
5. **ImprovementSuggestions** - Liste des suggestions

#### 3.3 Layout Principal (App.tsx)
```typescript
import { useState } from 'react';
import { CVUploader } from './components/upload/CVUploader';
import { JobDescriptionInput } from './components/upload/JobDescriptionInput';
import { AnalysisResults } from './components/results/AnalysisResults';
import { analyzeCV } from './services/api';

function App() {
  const [cvFile, setCvFile] = useState<File | null>(null);
  const [jobDescription, setJobDescription] = useState('');
  const [analysisResult, setAnalysisResult] = useState(null);
  const [loading, setLoading] = useState(false);

  const handleAnalyze = async () => {
    if (!cvFile || !jobDescription) return;
    
    setLoading(true);
    try {
      const result = await analyzeCV(cvFile, jobDescription);
      setAnalysisResult(result.analysis);
    } catch (error) {
      console.error('Analysis failed:', error);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-gray-50">
      <header className="bg-white shadow">
        <h1 className="text-3xl font-bold p-6">CV Analyzer</h1>
      </header>
      
      <main className="container mx-auto p-6">
        {!analysisResult ? (
          <div className="grid md:grid-cols-2 gap-6">
            <CVUploader onFileSelect={setCvFile} />
            <JobDescriptionInput 
              value={jobDescription}
              onChange={setJobDescription}
            />
            <button
              onClick={handleAnalyze}
              disabled={!cvFile || !jobDescription || loading}
              className="col-span-2 bg-blue-600 text-white py-3 rounded-lg"
            >
              {loading ? 'Analyzing...' : 'Analyze Match'}
            </button>
          </div>
        ) : (
          <AnalysisResults data={analysisResult} />
        )}
      </main>
    </div>
  );
}

export default App;
```

### Phase 4: Intégration & Tests (Jour 10-12)

#### 4.1 Tests Backend
```python
# tests/test_api.py

import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_health_check():
    response = client.get("/api/health")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"

def test_analyze_endpoint():
    # Créer un PDF de test
    with open("test_cv.pdf", "rb") as f:
        response = client.post(
            "/api/v1/analyze",
            files={"file": ("cv.pdf", f, "application/pdf")},
            data={
                "job_description": "Looking for a Python developer...",
                "language": "en"
            }
        )
    
    assert response.status_code == 200
    data = response.json()
    assert data["success"] == True
    assert "analysis" in data
```

#### 4.2 Tests d'Intégration
```bash
# scripts/test_integration.sh

#!/bin/bash

echo "Starting integration tests..."

# Start services
docker-compose up -d

# Wait for services to be ready
sleep 10

# Test health endpoint
curl http://localhost:8000/api/health

# Run pytest
docker-compose exec backend pytest

# Cleanup
docker-compose down

echo "Integration tests complete!"
```

### Phase 5: Optimisations & Polish (Jour 13-14)

#### 5.1 Caching avec Redis
```python
# app/services/cache_service.py

import redis
import json
from app.config import get_settings

settings = get_settings()
redis_client = redis.from_url(settings.redis_url)

def cache_analysis(key: str, data: dict, ttl: int = 3600):
    """Cache analysis result for 1 hour"""
    redis_client.setex(
        key,
        ttl,
        json.dumps(data)
    )

def get_cached_analysis(key: str):
    """Retrieve cached analysis"""
    cached = redis_client.get(key)
    if cached:
        return json.loads(cached)
    return None
```

#### 5.2 Rate Limiting
```python
# app/core/rate_limit.py

from fastapi import HTTPException
from slowapi import Limiter
from slowapi.util import get_remote_address

limiter = Limiter(key_func=get_remote_address)

@router.post("/analyze")
@limiter.limit("10/minute")
async def analyze_cv(...):
    # ... endpoint logic
```

#### 5.3 Logging
```python
# app/core/logging.py

import logging
from logging.handlers import RotatingFileHandler

def setup_logging():
    logger = logging.getLogger("cvanalyzer")
    logger.setLevel(logging.INFO)
    
    handler = RotatingFileHandler(
        "logs/app.log",
        maxBytes=10485760,  # 10MB
        backupCount=5
    )
    
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    
    return logger
```

---

## 📖 Guide de Démarrage

### Prerequisites
- Docker & Docker Compose installés
- Node.js 20+ (pour dev local)
- Python 3.11+ (pour dev local)
- Clés API Anthropic/OpenAI

### Installation

```bash
# 1. Cloner le repo
git clone <repo-url>
cd cv-analyzer-matching

# 2. Copier .env
cp .env.example .env

# 3. Éditer .env avec vos clés API
nano .env

# 4. Build et lancer avec Docker
docker-compose up --build

# 5. Accéder à l'application
# Frontend: http://localhost:3000
# Backend API: http://localhost:8000
# API Docs: http://localhost:8000/docs
```

### Développement Local (sans Docker)

#### Backend
```bash
cd backend
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python -m spacy download fr_core_news_lg
uvicorn app.main:app --reload
```

#### Frontend
```bash
cd frontend
npm install
npm run dev
```

---

## 🧪 Tests & Qualité

### Backend Tests
```bash
# Run all tests
docker-compose exec backend pytest

# With coverage
docker-compose exec backend pytest --cov=app

# Specific test
docker-compose exec backend pytest tests/test_api.py -v
```

### Frontend Tests
```bash
cd frontend
npm run test
npm run test:coverage
```

### Linting
```bash
# Backend
docker-compose exec backend black app/
docker-compose exec backend flake8 app/

# Frontend
cd frontend
npm run lint
npm run format
```

---


## 📈 Roadmap & Évolutions

### Version 1.1
- [ ] Support multi-langue (ES, DE, IT)
- [ ] Export PDF du rapport d'analyse
- [ ] Historique des analyses
- [ ] Comparaison de plusieurs CV

### Version 1.2
- [ ] Suggestions de formations (Coursera, Udemy)
- [ ] Templates de CV optimisés
- [ ] Extension Chrome pour analyse directe

### Version 2.0
- [ ] Matching automatique avec offres Indeed/LinkedIn
- [ ] AI-powered CV rewriting
- [ ] Interview preparation assistant
- [ ] Salary estimation based on profile

---

## 📚 Ressources Supplémentaires

### Documentation
- [FastAPI Docs](https://fastapi.tiangolo.com/)
- [React Docs](https://react.dev/)
- [spaCy Docs](https://spacy.io/)
- [Sentence Transformers](https://www.sbert.net/)
- [Chart.js](https://www.chartjs.org/)

### Modèles ML
- [Hugging Face Models](https://huggingface.co/models)
- [spaCy Models](https://spacy.io/models)

### APIs
- [Anthropic Claude](https://docs.anthropic.com/)
- [OpenAI](https://platform.openai.com/docs)

---

## ✨ Conclusion

Cette architecture fournit une base solide et scalable pour un système d'analyse de CV et matching d'offres. Les points clés:

✅ **Séparation des concerns** avec microservices  
✅ **NLP avancé** avec spaCy et sentence-transformers  
✅ **LLM Integration** pour suggestions intelligentes  
✅ **Visualisations riches** avec Chart.js  
✅ **Containerization** complète avec Docker  
✅ **API REST** bien documentée  
✅ **Frontend moderne** React + TypeScript  

Le projet est prêt pour le développement et l'évolution future !

---

**Happy Coding! 🚀**