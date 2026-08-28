<div align="center">

# 🧠 Personalized Learning Path Recommender

**An AI-powered platform that turns your career goals into a personalized, adaptive learning roadmap — powered by Gemini LLM, vector embeddings, and graph-based sequencing.**

[![Python](https://img.shields.io/badge/Python-3.12-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://python.org)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.115-009688?style=for-the-badge&logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com)
[![React](https://img.shields.io/badge/React-18-61DAFB?style=for-the-badge&logo=react&logoColor=black)](https://reactjs.org)
[![Gemini](https://img.shields.io/badge/Gemini_API-3.6_Flash-4285F4?style=for-the-badge&logo=google&logoColor=white)](https://ai.google.dev)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg?style=for-the-badge)](LICENSE)

[Report Bug](https://github.com/Samarth07-ctrl/personalized-learning-path-recommender/issues) · [Request Feature](https://github.com/Samarth07-ctrl/personalized-learning-path-recommender/issues)

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
| 🗣️ **Conversational Onboarding** | Chat-style UI that extracts your goals, current skills, time budget, and learning preferences via Gemini |
| 🧩 **Skill Gap Detection** | Compares your known skills against the target goal's prerequisite graph to compute exact gaps |
| 🔍 **Semantic Resource Retrieval** | Generates a rich query per skill and finds the most semantically relevant course via vector search |
| 🗺️ **Prerequisite-Ordered Roadmap** | NetworkX topological sort ensures you never see an advanced course before its prerequisites |
| 💡 **"Why this?" Explainability** | Slide-over panel on every course node explains exactly why it was recommended for your specific goal |
| 🔄 **Adaptive Feedback Loop** | **Complete** → skill mastered, next unlocked. **Skip** → alternative course fetched via vector search |
| 📊 **Dashboard & Radar Chart** | Visual progress tracking with skill radar and milestone progress bar |

---

## 🛠️ Tech Stack

### Backend
| Technology | Purpose |
|---|---|
| **FastAPI** | REST API framework |
| **SQLAlchemy + SQLite** | ORM & local database |
| **Gemini API** (`gemini-3.6-flash`) | LLM for profile extraction & explanations |
| **Gemini Embeddings** (`gemini-embedding-2`) | Course vectorization for semantic search |
| **NumPy** | Cosine similarity calculations |
| **NetworkX** | Prerequisite skill graph & topological sort |
| **python-dotenv** | Environment variable management |

### Frontend
| Technology | Purpose |
|---|---|
| **React 18 + Vite** | UI framework & build tool |
| **Tailwind CSS v4** | Styling |
| **React Router v6** | Client-side routing |
| **Recharts** | Skill radar & milestone progress charts |
| **Lucide React** | Icon library |

---

## 📁 Project Structure

```
HCL/
├── backend/
│   ├── main.py                          # FastAPI app & all API endpoints
│   ├── models.py                        # SQLAlchemy ORM models
│   ├── schemas.py                       # Pydantic request/response schemas
│   ├── database.py                      # DB connection & session
│   ├── seed_db.py                       # Seeds 50 courses with Gemini embeddings
│   └── services/
│       ├── ai_service.py                # Gemini LLM: profile extraction & explanations
│       ├── embedding_service.py         # Gemini Embeddings: vectorize & index courses
│       ├── graph_service.py             # NetworkX: skill gap & topological sort
│       └── recommendation_service.py   # Cosine similarity retrieval & ranking
│
├── frontend/
│   └── src/
│       ├── App.jsx                      # Router & navigation
│       └── components/
│           ├── OnboardingChat.jsx       # Conversational profile extraction UI
│           ├── RoadmapView.jsx          # Adaptive roadmap with slide-over panel
│           └── Dashboard.jsx           # Progress radar & milestone charts
│
├── .env.example                         # Template for required environment variables
├── .gitignore
└── PRD_AI_Learning_Path_Recommender.md # Product Requirements Document
```

---

## ⚙️ Setup & Installation

### Prerequisites
- Python 3.10+
- Node.js 18+
- A [Google AI Studio](https://aistudio.google.com/) API key

### 1. Clone the repository
```bash
git clone https://github.com/Samarth07-ctrl/personalized-learning-path-recommender.git
cd personalized-learning-path-recommender
```

### 2. Configure environment variables
```bash
cp .env.example .env
# Open .env and fill in your key:
# GEMINI_API_KEY=your_key_here
```

### 3. Set up the Backend
```bash
cd backend

# Create and activate virtual environment
python -m venv venv
.\venv\Scripts\Activate.ps1        # Windows
# source venv/bin/activate         # macOS/Linux

# Install dependencies
pip install fastapi uvicorn sqlalchemy pydantic python-dotenv google-generativeai numpy networkx

# Seed the database with 50 courses + Gemini embeddings (run once)
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

---

## 🔌 API Reference

| Method | Endpoint | Description |
|---|---|---|
| `GET` | `/` | Health check |
| `POST` | `/onboard` | Send chat messages → receive AI response + extracted learner profile |
| `GET` | `/profile/{id}` | Fetch a learner profile by ID |
| `POST` | `/path/generate` | Generate a personalized, prerequisite-ordered learning path |
| `POST` | `/progress/update` | Mark a course `completed` or `skipped`; triggers adaptive re-ranking |

---

## 🧠 AI/ML Pipeline In Detail

### 1. Intent & Profile Extraction
Every chat message is sent to `gemini-3.6-flash` with a strict structured-output prompt. The LLM returns a JSON object containing the extracted `goal`, `domain`, `current_level`, `known_skills`, and `time_budget`, plus the next follow-up question to ask.

### 2. Skill Gap Detection
The extracted `known_skills` are compared against the target goal's required skills in a NetworkX Directed Acyclic Graph (DAG). The gap set is the set of required skills the learner doesn't yet have.

### 3. Semantic Resource Retrieval
For each gap skill, a rich semantic query is constructed:
```
"machine_learning for an intermediate learner preparing for Become a Data Scientist"
```
This query is embedded using `gemini-embedding-2`, then Cosine Similarity is computed against all pre-indexed course vectors to retrieve the Top-K candidates. Metadata filtering and similarity scoring determine the final best resource.

### 4. Path Sequencing
NetworkX topological sort orders the skills by their prerequisite graph (e.g. `Statistics → Pandas → ML → Deep Learning`), ensuring the roadmap is always logically coherent.

### 5. Adaptive Feedback Loop
- **Complete**: Skill marked mastered in DB. Known skills updated. Next prerequisite node unlocked.
- **Skip**: New vector search runs for the *same skill*, excluding already-seen courses. Alternative resource swapped in. Only future nodes updated — completed history is preserved.

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
