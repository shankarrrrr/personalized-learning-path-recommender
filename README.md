<div align="center">

# 🧠 Personalized Learning Path Recommender

**An AI-powered platform that turns your career goals into a personalized, adaptive learning roadmap — powered by Gemini LLM, vector embeddings, and graph-based sequencing.**

[![Python](https://img.shields.io/badge/Python-3.11-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://python.org)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.115-009688?style=for-the-badge&logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com)
[![React](https://img.shields.io/badge/React-19-61DAFB?style=for-the-badge&logo=react&logoColor=black)](https://reactjs.org)
[![Gemini](https://img.shields.io/badge/Gemini_API-3.6_Flash-4285F4?style=for-the-badge&logo=google&logoColor=white)](https://ai.google.dev)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg?style=for-the-badge)](LICENSE)

[Report Bug](https://github.com/shankarrrrr/personalized-learning-path-recommender/issues) · [Request Feature](https://github.com/shankarrrrr/personalized-learning-path-recommender/issues)

</div>

---

## ✨ Overview

Most learning platforms give you the same generic catalog. This platform does something fundamentally different:

> You tell it your goal in plain English. It **understands** you, **maps your skill gaps**, and **builds a sequenced roadmap of the best resources** — then **adapts in real-time** as you learn.

Built for the **HCL Tech Hackathon**, this project demonstrates a production-quality AI/ML pipeline combining three distinct AI techniques:

1. **Large Language Model** (Gemini) for conversational profile extraction
2. **Semantic Vector Search** (Gemini Embeddings + Cosine Similarity) for resource retrieval
3. **Graph-Based Sequencing** (NetworkX DAG + Topological Sort) for prerequisite ordering

---

## 🏗️ Architecture

```
                        USER
                          │
                          ▼
               ┌─────────────────────┐
               │  Conversational UI  │  ← React + Vite
               │   (Onboarding Chat) │
               └──────────┬──────────┘
                          │ POST /onboard
                          ▼
               ┌─────────────────────┐
               │   Gemini LLM        │  ← gemini-3.6-flash
               │  Profile Extractor  │     Structured JSON Output
               └──────────┬──────────┘
                          │
                          ▼
               ┌─────────────────────┐
               │   Skill Gap Engine  │  ← NetworkX DAG
               │   (Graph Service)   │     Topological Sort
               └──────────┬──────────┘
                          │  For each required skill:
                          ▼
               ┌─────────────────────┐
               │  Vector Retrieval   │  ← gemini-embedding-2
               │  (Cosine Similarity)│     In-Memory Index
               └──────────┬──────────┘
                          │  Top-K candidates → Metadata Ranking
                          ▼
               ┌─────────────────────┐
               │  Personalized       │  ← Milestone grouping
               │  Learning Roadmap   │     Prerequisite-ordered
               └──────────┬──────────┘
                          │
                    ┌─────┴─────┐
                    ▼           ▼
              COMPLETE        SKIP
                    │           │
                    ▼           ▼
           Skill mastered   Vector search
           Next unlocked    finds alternative
                    │           │
                    └─────┬─────┘
                          ▼
               ┌─────────────────────┐
               │  Adaptive Roadmap   │  ← Only future nodes recalculated
               │  (Updated in-place) │     Completed history preserved
               └─────────────────────┘
```

---

## 🚀 Features

| Feature | Description |
|---|---|
| 🔐 **Authentication & Landing** | Login/register page is the app landing route (`/`); JWT-based auth persists sessions across refreshes |
| 🗣️ **Conversational Onboarding** | Chat-style UI that extracts your goals, current skills, time budget, and learning preferences via Gemini |
| 🧩 **Skill Gap Detection** | Compares your known skills against the target goal's prerequisite graph to compute exact gaps |
| 🔍 **Semantic Resource Retrieval** | Generates a rich query per skill and finds the most semantically relevant course via vector search |
| 🗺️ **Prerequisite-Ordered Roadmap** | NetworkX topological sort ensures you never see an advanced course before its prerequisites |
| 💡 **"Why this?" Explainability** | Slide-over panel on every course node explains exactly why it was recommended for your specific goal |
| 🔄 **Adaptive Feedback Loop** | **Complete** → skill mastered, next unlocked. **Skip** → alternative course fetched via vector search |
| 🧭 **Career Explorer** | Browse 11 career paths with filtering by domain, difficulty, salary, time, and remote-friendliness |
| 📊 **Dashboard & Radar Chart** | Visual progress tracking with skill radar, milestone progress bar, and peer recommendations |
| ⏱️ **Smart Recommendations** | Time-to-goal estimation, career-difficulty assessment, "people like you" suggestions, and alternative courses |

---

## 🛠️ Tech Stack

### Backend
| Technology | Purpose |
|---|---|
| **FastAPI** | REST API framework |
| **SQLAlchemy + SQLite** | ORM & local database |
| **Gemini API** (`gemini-3.6-flash`) | LLM for profile extraction & explanations |
| **Gemini Embeddings** (`gemini-embedding-2`) | Course vectorization for semantic search |
| **NumPy** | Vectorized cosine similarity |
| **NetworkX** | Prerequisite skill graph & topological sort |
| **python-jose + passlib (bcrypt)** | JWT auth & password hashing |
| **python-dotenv** | Environment variable management |

### Frontend
| Technology | Purpose |
|---|---|
| **React 19 + Vite** | UI framework & build tool |
| **Tailwind CSS v4** | Styling |
| **React Router v7** | Client-side routing |
| **Recharts** | Skill radar & milestone progress charts |
| **Lucide React** | Icon library |
| **Vitest + Testing Library** | Unit/component tests |

---

## 📁 Project Structure

```
personalized-learning-path-recommender/
├── backend/
│   ├── main.py                          # FastAPI app & all API endpoints
│   ├── models.py                        # SQLAlchemy ORM models
│   ├── schemas.py                       # Pydantic request/response schemas
│   ├── database.py                      # DB connection & session
│   ├── auth_deps.py                     # JWT auth FastAPI dependencies
│   ├── error_handlers.py                # Centralized exception handlers
│   ├── seed_db.py                       # Seeds 104 courses + 11 careers with Gemini embeddings
│   ├── data/                            # Curated real-course & career-path seed data
│   ├── services/
│   │   ├── ai_service.py                # Gemini LLM: profile extraction & explanations
│   │   ├── embedding_service.py          # Gemini Embeddings: vectorize & index courses
│   │   ├── graph_service.py             # NetworkX: skill gap & topological sort
│   │   ├── recommendation_service.py    # Cosine similarity retrieval & ranking
│   │   ├── recommendation_engine.py     # Smart recommendations (time/difficulty/peers)
│   │   ├── auth_service.py              # Password hashing & JWT tokens
│   │   └── cache.py                     # In-memory TTL cache
│   └── tests/                           # pytest suite (64 tests)
│
├── frontend/
│   └── src/
│       ├── App.jsx                      # Router, navigation & route table
│       ├── lib/
│       │   ├── api.js                   # Centralized fetch client w/ error handling
│       │   └── auth.jsx                 # Auth context (login/register/logout)
│       ├── components/
│       │   ├── AuthPage.jsx             # Login/register (app landing page)
│       │   ├── OnboardingChat.jsx       # Conversational profile extraction UI
│       │   ├── RoadmapView.jsx          # Adaptive roadmap with slide-over panel
│       │   ├── CareerExplorer.jsx       # Career browsing with filters
│       │   ├── Dashboard.jsx            # Progress radar & milestone charts
│       │   ├── CourseCard.jsx           # Reusable course card
│       │   ├── Toast.jsx                # Toast notifications
│       │   ├── ErrorBoundary.jsx        # Render-error fallback
│       │   └── Skeletons.jsx            # Loading placeholders
│       └── test/                       # Vitest suite (31 tests)
│
├── .env.example                         # Template for required environment variables
├── .gitignore
├── docker-compose.yml                   # Production backend + frontend containers
└── PRD_AI_Learning_Path_Recommender.md  # Product Requirements Document
```

---

## ⚙️ Setup & Installation

### Prerequisites
- Python 3.11+
- Node.js 18+
- A [Google AI Studio](https://aistudio.google.com/) API key

### 1. Clone the repository
```bash
git clone https://github.com/shankarrrrr/personalized-learning-path-recommender.git
cd personalized-learning-path-recommender
```

### 2. Configure environment variables
```bash
cp .env.example .env        # macOS/Linux
copy .env.example .env      # Windows
# Open .env and fill in your key:
# GEMINI_API_KEY=your_key_here
```

### 3. Set up the Backend
```bash
cd backend

# (Optional) create and activate a virtual environment
python -m venv venv
.\venv\Scripts\Activate.ps1        # Windows
# source venv/bin/activate         # macOS/Linux

# Install dependencies (pinned for reproducibility)
pip install -r requirements.txt

# Seed the database with 104 courses + 11 career paths (run once)
python seed_db.py

# Start the backend server
uvicorn main:app --reload
# → API running at http://127.0.0.1:8000
```

### 4. Set up the Frontend
```bash
cd frontend
npm install
npm run dev
# → App running at http://localhost:5173
```

The app now opens on the **login page**. Register an account (or click "Continue without an account" to use the chat onboarding anonymously).

---

## 🔌 API Reference

### Core
| Method | Endpoint | Description |
|---|---|---|
| `GET` | `/` | Root health check |
| `GET` | `/health` | Service + dependency health (DB, AI, course count) |
| `POST` | `/auth/register` | Register a new user, returns JWT |
| `POST` | `/auth/login` | Authenticate a user, returns JWT |
| `GET` | `/auth/me` | Current authenticated user |
| `POST` | `/onboard` | Chat messages → AI response + extracted learner profile |
| `GET` | `/profile/{id}` | Fetch a learner profile by ID |
| `POST` | `/path/generate` | Generate a personalized, prerequisite-ordered learning path |
| `POST` | `/progress/update` | Mark a course `completed` or `skipped`; triggers adaptive re-ranking |
| `GET` | `/analytics/progress/{learner_id}` | Skill radar, milestone progress, next action, summary |

### Careers
| Method | Endpoint | Description |
|---|---|---|
| `GET` | `/careers` | List career paths (filterable: domain, difficulty, salary, time, remote) |
| `GET` | `/careers/{id}` | Get a career path by ID |
| `GET` | `/careers/domains/list` | All unique career domains |
| `GET` | `/careers/stats/summary` | Aggregate career stats |
| `POST` | `/careers/{id}/select` | Select a career, update profile, and generate a learning path |

### Recommendations
| Method | Endpoint | Description |
|---|---|---|
| `GET` | `/recommendations/time-to-goal/{learner_id}` | Estimate weeks/months to reach the learner's goal |
| `GET` | `/recommendations/career-difficulty/{career_id}` | Assess how hard a career will be for the learner |
| `GET` | `/recommendations/people-like-you/{learner_id}` | Courses studied by learners with overlapping interests |
| `GET` | `/recommendations/alternatives/{skill_id}` | Alternative courses for a skill (skip flow) |
| `GET` | `/recommendations/explain` | One-line AI rationale for why a course was recommended |

---

## 🧠 AI/ML Pipeline In Detail

### 1. Intent & Profile Extraction
Every chat message is sent to `gemini-3.6-flash` with a strict structured-output prompt. The LLM returns a JSON object containing the extracted `goal`, `domain`, `current_level`, `known_skills`, and `time_budget`, plus the next follow-up question to ask and career suggestions.

### 2. Skill Gap Detection
The extracted `known_skills` are compared against the target goal's required skills in a NetworkX Directed Acyclic Graph (DAG). The gap set is the set of required skills (and their prerequisites) the learner doesn't yet have.

### 3. Semantic Resource Retrieval
For each gap skill, a rich semantic query is constructed:
```
"machine_learning for an intermediate learner preparing for Become a Data Scientist"
```
This query is embedded using `gemini-embedding-2`, then Cosine Similarity is computed (vectorized with NumPy) against all pre-indexed course vectors to retrieve the best candidate. Metadata boosting (e.g. preferred format) refines the final pick.

### 4. Path Sequencing
NetworkX topological sort orders the skills by their prerequisite graph (e.g. `Statistics → Pandas → ML → Deep Learning`), ensuring the roadmap is always logically coherent.

### 5. Adaptive Feedback Loop
- **Complete**: Skill marked mastered in DB. Known skills updated. Next prerequisite node unlocked.
- **Skip**: New vector search runs for the *same skill*, excluding already-seen courses. Alternative resource swapped in. Only future nodes updated — completed history is preserved.

### 6. Embedding Cache (session-safe)
Course vectors are cached in memory as detached snapshots so retrieval stays fast across requests without re-querying the DB or re-hitting the embedding API. The cache stores session-independent snapshots (not ORM objects), so it never triggers detached-instance errors across requests.

---

## 🧪 Testing

### Backend (pytest)
```bash
cd backend
pip install -r requirements.txt
pytest              # 64 tests across API, auth, cache, graph, recommendations
```

### Frontend (Vitest)
```bash
cd frontend
npm install
npm test            # 31 tests across API client, Toast, CourseCard, ErrorBoundary
```

---

## 🐳 Docker

Run the full stack in containers:
```bash
GEMINI_API_KEY=your_key docker compose up --build
# → Backend at http://localhost:8000
# → Frontend at http://localhost:8080
```

---

## 🤝 Contributing

1. Fork the project
2. Create your feature branch: `git checkout -b feature/AmazingFeature`
3. Commit your changes: `git commit -m 'Add some AmazingFeature'`
4. Push to the branch: `git push origin feature/AmazingFeature`
5. Open a Pull Request

---

## 📄 License

Distributed under the MIT License.

---

<div align="center">

Built with ❤️ for the **HCL Tech Hackathon**

</div>
