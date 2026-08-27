# PRD — AI-Powered Personalized Learning Path Recommender

**Version:** 1.0 · **Prepared for:** Hackathon Round 2 build · **Date:** Aug 27, 2026

---

## 1. Executive Summary

An AI-powered assistant that takes a learner's goals, current skills, and history (via natural conversation) and produces a personalized, sequenced learning roadmap — courses, projects, and assessments — with explanations for every recommendation and a dashboard that adapts as the learner progresses.

The system is judged on: problem understanding (20%), functionality (25%), AI/ML depth (20%), innovation (15%), UX (10%), code quality (10%). This PRD is structured so the build order directly maximizes those weights within a hackathon timeframe.

---

## 2. Problem Statement

Learners on large course catalogs face **choice overload**: they can find individual courses but not the *right sequence* to reach a goal. Needs vary by skill level, prior learning, career aspiration, and learning style — a static "top courses" list doesn't solve this. The gap is **sequencing + personalization + explainability**, not discovery.

---

## 3. Goals & Success Metrics

| Goal | Metric (for demo / judging) |
|---|---|
| Understand learner intent from free text | Correctly extracts goal, level, interests in ≥90% of test prompts |
| Generate a coherent roadmap | Path respects prerequisite order; no circular/broken dependencies |
| Explain recommendations | Every node in the path has a natural-language "why" |
| Adapt to feedback/progress | Marking a course complete/skipped visibly re-ranks remaining path |
| Deliver a working demo | End-to-end flow: onboarding → path → dashboard, in under 5 min |

---

## 4. User Personas

1. **Career switcher** — e.g., marketing → data analytics. Needs foundational sequencing, doesn't know what they don't know.
2. **Upskilling professional** — already has a base (e.g., Python dev wanting ML). Needs gap-filling, not a full beginner path.
3. **Student with a deadline** — exam/certification goal, needs time-boxed milestones.

Use these three to validate your recommendation engine covers "beginner from zero," "gap-fill from existing skill," and "goal-constrained by time."

---

## 5. Scope for Hackathon (MVP vs Stretch)

**MVP (must work in the demo):**
- Conversational onboarding (goal, level, interests, time available)
- Learner profile object (structured, stored)
- Course/resource dataset (seeded, 50–150 items across 2–3 domains is enough — don't try to cover "all domains")
- Path generator with prerequisite ordering and milestones
- "Why this?" explanation per recommendation
- Dashboard: path view + progress + skill radar/bar
- Feedback loop: mark complete → path re-ranks or adjusts

**Stretch (only if MVP is solid):**
- Multi-domain support
- Real course API integration (Coursera/edX/YouTube metadata)
- Skill-gap radar chart with live updates
- Spaced-repetition style resource resurfacing
- Voice input

**Explicitly out of scope for hackathon:** payments, real user auth/SSO, content authoring tools, mobile app.

---

## 6. Functional Requirements (mapped to "what to build")

### 6.1 Conversational Interface
- Chat-style UI where learner describes goals in natural language ("I want to become a data analyst in 3 months, I know basic Excel").
- LLM extracts structured fields: `goal`, `domain`, `current_level`, `time_budget`, `interests`, `preferred_format` (video/text/project-based).
- Follow-up questions if fields are missing (e.g., "What's your current experience with SQL?").
- Ongoing chat also used post-onboarding for Q&A about the path.

### 6.2 Learner Profiling Engine
- Structured profile built from conversation + optional explicit form (experience level, completed courses, objectives).
- Profile is persisted and updated over time (not just onboarding — every interaction can refine it).
- Skill vector: per-topic proficiency estimate (self-reported initially, adjusted by quiz/assessment results later).

### 6.3 Recommendation Engine
- Course/resource corpus embedded (vector representations of title, description, skills taught, prerequisites, difficulty).
- Given learner profile + goal, retrieve candidate resources via semantic similarity + metadata filtering (level, format, domain).
- Rank candidates by relevance to goal and skill-gap coverage.

### 6.4 Learning Path Generator
- Build a directed graph of skills/topics with prerequisite edges (a small hand-curated knowledge graph per domain is fine for hackathon scope).
- Topologically sort required skills for the goal, subtract skills the learner already has, map remaining skills to recommended resources.
- Group into milestones (e.g., "Milestone 1: Python fundamentals," "Milestone 2: Data manipulation with pandas").
- Output: ordered roadmap with prerequisites, estimated time, and milestone checkpoints.

### 6.5 Explainability & Assistant Q&A
- For each recommended resource: short LLM-generated rationale referencing the learner's stated goal/gap ("Recommended because you said you want to work with data pipelines, and this closes your SQL gap before the pandas module").
- Chat remains available to ask "why not X" or "can I skip this."

### 6.6 Progress Dashboard
- Visual roadmap (timeline or graph view) with status per node (locked / in progress / done).
- Skill development view (simple bar/radar per skill area).
- "Next recommended action" panel.
- Milestone completion indicators.

---

## 7. System Architecture

```
Frontend (React)
     │
API Gateway / Backend (FastAPI or Node/Express)
     │
 ┌───┴─────────────────────────────────────────┐
 │              AI / ML Services                │
 │  Conversational   Recommendation   Path        │
 │  understanding    engine (vector   generator    │
 │  (LLM intent      search)          (graph +      │
 │  extraction)                       topo sort)     │
 │  Explainability agent   Adaptive feedback loop     │
 └───┬─────────────────────────────────────────┘
     │
Data layer: learner profiles · course catalog · vector store · progress logs
     │
External: course metadata sources · skill taxonomy · LLM API
```

**Design principle:** keep AI/ML services as separate, composable modules (not one giant prompt) — this is what judges reward under "AI/ML Implementation" and makes the system debuggable during a live demo.

---

## 8. Tech Stack (recommended for a hackathon timeline)

| Layer | Choice | Why |
|---|---|---|
| Frontend | React + Tailwind CSS | Fast to build, good for chat + dashboard UI |
| Backend/API | FastAPI (Python) | Easy LLM/ML integration, async, quick to stand up |
| LLM | Anthropic Claude API (or OpenAI) | Conversational extraction, explanations, Q&A |
| Embeddings/Vector search | OpenAI/Voyage embeddings + FAISS or Chroma (local, no infra) | Fast semantic course retrieval, zero-ops for a hackathon |
| Knowledge graph | NetworkX (Python) over a hand-curated JSON skill/prereq graph | Simple prerequisite sequencing without a graph DB |
| Database | PostgreSQL (or SQLite for speed) + Prisma/SQLAlchemy | Learner profiles, progress, course metadata |
| Auth | Simple JWT or even a mock/local session for demo | Don't over-invest here |
| Charts | Recharts / Chart.js | Skill radar, progress bars |
| Deployment | Vercel (frontend) + Railway/Render (backend) | Fast, free-tier deploy for a public demo URL |
| Version control | GitHub, with clear commit history | Required deliverable |

**Why not a full graph database (Neo4j) or heavy MLOps stack:** for a hackathon, a JSON-based prerequisite graph + vector store gives 90% of the value with a fraction of the setup time. Reserve Neo4j as a stretch/"future work" architecture slide.

---

## 9. AI/ML Approach in Detail

1. **Intent & profile extraction:** prompt the LLM with a structured-output instruction (JSON schema for goal, level, interests, time budget). Use function-calling / structured output rather than free text parsing.
2. **Skill-gap detection:** compare extracted "known skills" against the target goal's required-skill list (from the knowledge graph) to compute the gap set.
3. **Recommendation retrieval:** embed course descriptions once (offline/setup step); embed the gap skills + learner interests at query time; cosine similarity search; filter by level/format metadata.
4. **Path sequencing:** topological sort over the prerequisite graph restricted to the gap set; group into milestones by logical clusters (e.g., every 3–4 resources or by topic cluster).
5. **Explanation generation:** for each selected resource, a short LLM call (or templated + LLM-polished) referencing the specific gap/goal it addresses — avoid generic boilerplate.
6. **Adaptive feedback loop:** when a learner marks a course done/skipped or performs poorly on an optional quiz, update the skill vector and re-run steps 3–4 for the remaining path (not the whole path — only what's ahead, so progress feels stable, not chaotic).

This gives you three distinct, demoable AI/ML techniques (LLM structured extraction, embedding-based retrieval, graph-based sequencing) plus a feedback loop — strong coverage for the AI/ML Implementation criterion.

---

## 10. Data Model (core entities)

- **LearnerProfile**: id, goal, domain, current_level, known_skills[], interests[], time_budget, preferred_format, created_at
- **Course**: id, title, description, domain, skills_taught[], prerequisites[], level, format, duration, embedding_vector
- **SkillNode**: id, name, domain, prerequisite_skill_ids[]
- **LearningPath**: id, learner_id, ordered_nodes[] (skill_id, course_id, status, milestone_id), generated_at
- **ProgressLog**: id, learner_id, course_id, status (locked/in_progress/done/skipped), timestamp, optional_score

---

## 11. Key API Endpoints (illustrative)

```
POST /onboard              → conversational turn, returns updated profile + next question or "profile complete"
GET  /profile/:id          → learner profile
POST /path/generate        → generates/regenerates path for a learner
GET  /path/:learner_id     → current roadmap
POST /progress/update      → mark a node complete/skipped, triggers re-rank
GET  /explain/:node_id     → why this recommendation
POST /chat                 → free-form Q&A about the path
```

---

## 12. UX Notes

- Chat-first onboarding, but allow a quick structured form as a fallback/shortcut.
- Roadmap view: timeline or step-graph (locked/current/done states visually distinct).
- Dashboard: one skill-progress visual + "what's next" card is enough — don't over-build widgets, judges weight UX at only 10%.
- Every recommendation card should have a one-line "why" visible without a click — this directly demonstrates the explainability requirement.

---

## 13. Suggested Hackathon Timeline

| Phase | Focus |
|---|---|
| Day 1 AM | Finalize scope, data schema, seed course dataset (1–2 domains), skill/prereq graph |
| Day 1 PM | Backend: profile extraction endpoint, embeddings + vector search working end-to-end |
| Day 2 AM | Path generator (topo sort + milestone grouping) + explanation generation |
| Day 2 PM | Frontend: chat UI + roadmap view wired to backend |
| Day 3 AM | Dashboard (progress/skill viz) + feedback loop (re-ranking on progress update) |
| Day 3 PM | Polish, deploy, record demo video, write documentation |

Adjust to your actual hackathon length — the order (data → backend core loop → frontend → adaptive loop → polish) stays the same regardless of total days.

---

## 14. Risks & Mitigations

| Risk | Mitigation |
|---|---|
| Course dataset too thin to feel "real" | Seed with a curated 100–150 item set across 2 domains rather than trying to be comprehensive |
| LLM extraction misses fields | Always allow explicit form fallback; validate JSON output, retry on malformed responses |
| Path generator produces illogical order | Hand-verify the prerequisite graph for your demo domains before building on top of it |
| Over-scoping under time pressure | Cut stretch features first (multi-domain, live APIs) — never cut explainability or the feedback loop, since those map directly to judged criteria |

---

## 15. Deliverables Checklist (per submission guidelines)

- [ ] Source code ZIP (exclude venvs/node_modules/build artifacts) + README with setup/run instructions
- [ ] GitHub repo, public/accessible, with incremental commit history
- [ ] Solution documentation (PDF/PPT): problem understanding, approach, architecture, AI/ML techniques, features, workflows, challenges
- [ ] 3–5 min demo video: full flow (onboarding → roadmap → explanation → progress update → dashboard change)
- [ ] Deployed app URL (Vercel/Render) or clear local setup instructions if not deployed

---

## 16. Judging Criteria Alignment (self-check before submission)

| Criterion | Weight | Where it's addressed |
|---|---|---|
| Problem Understanding & Solution Design | 20% | §2–5 |
| Functionality & Feature Completeness | 25% | §6, all six required modules |
| AI/ML Implementation | 20% | §9 — three distinct techniques + feedback loop |
| Innovation & Creativity | 15% | Explainability agent, adaptive re-ranking, milestone clustering |
| User Experience & Interface | 10% | §12 |
| Performance & Code Quality | 10% | §8 stack choices, §11 clean API design, README quality |
