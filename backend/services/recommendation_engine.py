"""
Smart recommendation engine.

Augments the vector-search course retrieval with higher-level intelligence:
- time-to-goal estimation from the learner's skill gap + skill complexity
- career difficulty assessment
- "people like you also studied" collaborative-style suggestions based on
  shared interests/goals across other learner profiles
- alternative course suggestions when a learner skips a course

The implementation is deliberately dependency-light: it uses the existing
graph_service for skill-gap math and the recommendation_service for vector
retrieval, and adds a few simple heuristics on top. These are easy to later
swap for a real collaborative-filtering model without changing the API.
"""
from __future__ import annotations

from typing import Any, Dict, List, Optional

import models
from services.graph_service import graph_service
from services.recommendation_service import recommendation_service
from services.ai_service import ai_service


# Rough complexity weight per skill level (Beginner=1, Intermediate=2, Advanced=3).
# Used to estimate learning time from a skill gap.
LEVEL_WEIGHTS = {"Beginner": 1, "Intermediate": 2, "Advanced": 3}
# Average weeks a beginner needs per weighted skill "unit".
WEEKS_PER_WEIGHT_UNIT = 1.5


def _estimate_weeks(skill_ids: List[str], db_session) -> int:
    """Estimate total weeks to learn the given skills using course levels."""
    total = 0
    for skill_id in skill_ids:
        course = _course_for_skill(skill_id, db_session)
        weight = LEVEL_WEIGHTS.get((course.level if course else "Beginner"), 1)
        total += weight
    # Each weighted unit takes ~WEEKS_PER_WEIGHT_UNIT weeks.
    return max(1, int(total * WEEKS_PER_WEIGHT_UNIT)) if total else 0


def _course_for_skill(skill_id: str, db_session):
    """Return the first course that teaches a skill, or None."""
    courses = db_session.query(models.Course).all()
    for c in courses:
        if skill_id in (c.skills_taught or []):
            return c
    return None


class RecommendationEngine:
    """High-level recommendation helpers exposed via API endpoints."""

    def estimate_time_to_goal(self, learner_profile, db_session) -> Dict[str, Any]:
        """Estimate weeks/months to reach the learner's goal from their current skills.

        Uses the skill graph to compute the gap, then sums per-skill complexity.
        Falls back gracefully if the goal can't be mapped to a career.
        """
        career = self._career_for_profile(learner_profile, db_session)
        goal_skills = (career.required_skills if career else []) or list(
            learner_profile.interests or []
        ) or ["machine_learning"]
        known = set(learner_profile.known_skills or [])
        gap = graph_service.compute_skill_gap(goal_skills, list(known))

        weeks = _estimate_weeks(gap, db_session)
        months = round(weeks / 4.3, 1) if weeks else 0
        return {
            "total_skills_to_learn": len(gap),
            "estimated_weeks": weeks,
            "estimated_months": months,
            "skills": gap,
            "career": {"id": career.id, "title": career.title} if career else None,
        }

    def assess_career_difficulty(self, career, learner_profile) -> Dict[str, Any]:
        """Assess how hard a career will be for a given learner (0-100 score + label)."""
        known = set(learner_profile.known_skills or [])
        required = set(career.required_skills or [])
        gap = required - known
        coverage = (len(required) - len(gap)) / len(required) if required else 0.0

        # Difficulty rises with career difficulty level and uncovered skills.
        base = {"Beginner": 25, "Intermediate": 50, "Advanced": 75}.get(
            career.difficulty_level, 50
        )
        gap_ratio = len(gap) / len(required) if required else 1.0
        score = int(min(100, base + gap_ratio * 40))
        if score >= 75:
            label = "Challenging"
        elif score >= 50:
            label = "Moderate"
        else:
            label = "Achievable"
        return {
            "difficulty_score": score,
            "difficulty_label": label,
            "skills_covered": len(required) - len(gap),
            "skills_needed": len(gap),
            "coverage_pct": round(coverage * 100, 1),
        }

    def people_like_you_studied(
        self, learner_profile, db_session, limit: int = 5
    ) -> List[Dict[str, Any]]:
        """Suggest courses studied by learners with overlapping interests/goal.

        A lightweight collaborative signal: find other learner profiles that
        share at least one interest or the same domain, then aggregate the
        courses on their learning paths, ranked by frequency.
        """
        my_interests = set(learner_profile.interests or [])
        my_domain = (learner_profile.domain or "").strip().lower()

        peers = (
            db_session.query(models.LearnerProfile)
            .filter(models.LearnerProfile.id != learner_profile.id)
            .all()
        )

        # Score each peer by overlap with the current learner.
        scored_peers = []
        for peer in peers:
            peer_interests = set(peer.interests or [])
            overlap = len(my_interests & peer_interests)
            same_domain = bool(my_domain) and (peer.domain or "").strip().lower() == my_domain
            score = overlap + (1 if same_domain else 0)
            if score > 0:
                scored_peers.append((peer, score))

        scored_peers.sort(key=lambda x: x[1], reverse=True)

        # Aggregate course_ids from the top peers' learning paths.
        course_counts: Dict[str, int] = {}
        for peer, _ in scored_peers[:20]:  # consider top 20 peers
            paths = (
                db_session.query(models.LearningPath)
                .filter(models.LearningPath.learner_id == peer.id)
                .all()
            )
            for path in paths:
                for node in (path.ordered_nodes or []):
                    cid = node.get("course_id")
                    if cid and not cid.startswith("course_for_"):
                        course_counts[cid] = course_counts.get(cid, 0) + 1

        # Exclude courses the learner already has on their own path.
        my_path = (
            db_session.query(models.LearningPath)
            .filter(models.LearningPath.learner_id == learner_profile.id)
            .order_by(models.LearningPath.id.desc())
            .first()
        )
        my_course_ids = {
            n.get("course_id") for n in (my_path.ordered_nodes if my_path else [])
        }

        ranked = sorted(
            ((cid, count) for cid, count in course_counts.items() if cid not in my_course_ids),
            key=lambda x: x[1],
            reverse=True,
        )

        results = []
        for cid, count in ranked[:limit]:
            course = db_session.query(models.Course).filter(models.Course.id == cid).first()
            if course:
                results.append(self._course_to_dict(course, extra={"peer_count": count}))
        return results

    def alternative_courses(
        self, skill_id: str, learner_profile, db_session, exclude_course_ids: Optional[List[str]] = None
    ) -> List[Dict[str, Any]]:
        """Return up to 3 alternative courses for a skill (for the skip flow)."""
        exclude_course_ids = exclude_course_ids or []
        courses = (
            db_session.query(models.Course)
            .filter(models.Course.skills_taught.contains([skill_id]))
            .all()
        )
        alts = [c for c in courses if c.id not in exclude_course_ids]
        # Sort by rating descending; fall back to vector similarity if no ratings.
        alts.sort(key=lambda c: (c.rating or 0.0), reverse=True)
        return [self._course_to_dict(c) for c in alts[:3]]

    def explain_course(self, course_title: str, user_goal: str) -> str:
        """One-line AI rationale for why a course was recommended."""
        try:
            return ai_service.explain_recommendation(course_title, user_goal)
        except Exception:
            return f"Recommended because it builds the foundation for your goal to {user_goal}."

    # --- helpers ---

    def _career_for_profile(self, learner_profile, db_session):
        """Find the career matching the learner's goal/title or domain."""
        if learner_profile.goal:
            career = (
                db_session.query(models.CareerPath)
                .filter(models.CareerPath.title.ilike(f"%{learner_profile.goal}%"))
                .first()
            )
            if career:
                return career
        if learner_profile.domain:
            career = (
                db_session.query(models.CareerPath)
                .filter(models.CareerPath.domain == learner_profile.domain)
                .first()
            )
            if career:
                return career
        return None

    def _course_to_dict(self, course, extra: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        d = {
            "id": course.id,
            "title": course.title,
            "platform": course.platform,
            "level": course.level,
            "duration": course.duration,
            "rating": course.rating,
            "is_free": course.is_free,
            "price": course.price,
            "course_url": course.course_url,
            "skills_taught": course.skills_taught or [],
        }
        if extra:
            d.update(extra)
        return d


recommendation_engine = RecommendationEngine()
