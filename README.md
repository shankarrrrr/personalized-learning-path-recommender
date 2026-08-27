# AI-Powered Personalized Learning Path Recommender

An AI-driven educational platform designed to build personalized learning roadmaps based on a user's unique goals, current skills, and time constraints. Built for a Hackathon environment, this project demonstrates an end-to-end architecture encompassing conversational intent extraction, vector-based semantic recommendations, and graph-based prerequisite topological sorting.

## 🚀 Features

- **Conversational Onboarding:** Chat with an AI assistant to easily extract your goals and constraints.
- **Dynamic Learning Paths:** Generates a personalized timeline of milestones using a topological sort on prerequisite skill graphs.
- **Explainability Panel:** Contextual "Why this?" explanations generated for every recommendation to ensure trust.
- **Skill Radar Dashboard:** Visualizes your growing skill set and tracks milestone progress dynamically as you mark nodes complete.
- **Adaptive Feedback Loop:** The learning path re-calculates remaining steps dynamically if you skip or complete content faster than expected.

## 🛠️ Tech Stack

### Frontend
- **Framework:** React + Vite
- **Styling:** Tailwind CSS (Custom AI-native design system)
- **Icons & Charts:** Lucide React, Recharts
- **Routing:** React Router DOM

### Backend
- **Framework:** FastAPI (Python)
- **Database:** SQLite with SQLAlchemy ORM
- **AI/ML:** Prepared for OpenAI/Anthropic SDK integrations
- **Algorithms:** NetworkX for prerequisite graph traversal

## 📂 Project Structure

```
.
├── frontend/               # React + Vite application
│   ├── src/
│   │   ├── components/     # Reusable UI elements (Chat, Roadmap, Dashboard)
│   │   ├── index.css       # Tailwind configuration and base styles
│   │   └── App.jsx         # Main router and layout
├── backend/                # FastAPI application
│   ├── main.py             # API endpoints
│   ├── models.py           # SQLAlchemy database models
│   ├── schemas.py          # Pydantic schemas for data validation
│   └── services/           # AI, Graph, and DB services
└── README.md
```

## 🏁 Getting Started

### Prerequisites
- Node.js (v18+)
- Python (3.10+)

### 1. Frontend Setup
Navigate to the frontend directory and start the Vite dev server:
```bash
cd frontend
npm install
npm run dev
```
The frontend will run at `http://localhost:5173/`.

### 2. Backend Setup
Navigate to the backend directory, set up your virtual environment, and start the FastAPI server:
```bash
cd backend
python -m venv venv

# Activate the virtual environment
# Windows:
.\venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install fastapi uvicorn sqlalchemy pydantic openai anthropic networkx

# Run the server
uvicorn main:app --reload
```
The backend API will run at `http://127.0.0.1:8000/`. You can view the automatic Swagger UI documentation at `http://127.0.0.1:8000/docs`.

## 🤝 Contributing
Contributions, issues, and feature requests are welcome!

## 📝 License
This project is open-source and available under the MIT License.
