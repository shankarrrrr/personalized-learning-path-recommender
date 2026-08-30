"""Tests for the smart recommendation engine.

These tests use the seeded in-memory data and avoid real AI calls by
monkeypatching the ai_service.explain_recommendation fallback.
"""
import pytest

import models
from services.recommendation_engine import recommendation_engine


class TestTimeToGoal:
    def test_estimate_for_known_career(self, db_session):
        profile = models.LearnerProfile(goal="Data Scientist", domain="Data Science")
        db_session.add(profile)
        db_session.commit()
        result = recommendation_engine.estimate_time_to_goal(profile, db_session)
        assert result["career"] is not None
        assert result["career"]["id"] == "data_scientist"
        assert result["total_skills_to_learn"] > 0
        assert result["estimated_weeks"] > 0
        assert result["estimated_months"] > 0
        assert "machine_learning" in result["skills"]

    def test_estimate_respects_known_skills(self, db_session):
        profile = models.LearnerProfile(
            goal="Data Scientist", known_skills=["python_basics", "statistics"]
        )
        db_session.add(profile)
        db_session.commit()
        result = recommendation_engine.estimate_time_to_goal(profile, db_session)
        # Known skills should not appear in the gap.
        assert "python_basics" not in result["skills"]
        assert "statistics" not in result["skills"]

    def test_estimate_falls_back_to_interests(self, db_session):
        """No career match -> use interests as goal skills."""
        profile = models.LearnerProfile(
            goal="Unknown Role", interests=["python_basics"],
        )
        db_session.add(profile)
        db_session.commit()
        result = recommendation_engine.estimate_time_to_goal(profile, db_session)
        assert result["career"] is None
        assert "python_basics" in result["skills"]


class TestCareerDifficulty:
    def test_fresh_learner_is_challenging(self, db_session):
        profile = models.LearnerProfile(known_skills=[])
        db_session.add(profile)
        db_session.commit()
        career = db_session.query(models.CareerPath).first()
        result = recommendation_engine.assess_career_difficulty(career, profile)
        assert result["difficulty_label"] == "Challenging"
        assert result["coverage_pct"] == 0.0
        assert result["skills_needed"] == len(career.required_skills)

    def test_full_coverage_is_achievable(self, db_session):
        career = db_session.query(models.CareerPath).first()
        profile = models.LearnerProfile(known_skills=list(career.required_skills))
        db_session.add(profile)
        db_session.commit()
        result = recommendation_engine.assess_career_difficulty(career, profile)
        assert result["coverage_pct"] == 100.0
        assert result["difficulty_label"] == "Achievable"


class TestAlternativeCourses:
    def test_returns_alternatives_for_skill(self, db_session):
        profile = models.LearnerProfile()
        db_session.add(profile)
        db_session.commit()
        alts = recommendation_engine.alternative_courses("python_basics", profile, db_session)
        assert len(alts) >= 1
        assert alts[0]["id"] == "python_basics"

    def test_excludes_requested_ids(self, db_session):
        profile = models.LearnerProfile()
        db_session.add(profile)
        db_session.commit()
        alts = recommendation_engine.alternative_courses(
            "python_basics", profile, db_session, exclude_course_ids=["python_basics"]
        )
        assert all(a["id"] != "python_basics" for a in alts)


class TestExplainCourse:
    def test_explain_uses_ai_service(self, db_session, monkeypatch):
        captured = {}

        def fake_explain(title, goal):
            captured["title"] = title
            captured["goal"] = goal
            return "AI-generated rationale."

        monkeypatch.setattr(
            "services.recommendation_engine.ai_service.explain_recommendation",
            fake_explain,
        )
        result = recommendation_engine.explain_course("Python for Everybody", "Data Scientist")
        assert result == "AI-generated rationale."
        assert captured["title"] == "Python for Everybody"
        assert captured["goal"] == "Data Scientist"

    def test_explain_falls_back_on_ai_error(self, db_session, monkeypatch):
        def raising_explain(title, goal):
            raise RuntimeError("AI down")

        monkeypatch.setattr(
            "services.recommendation_engine.ai_service.explain_recommendation",
            raising_explain,
        )
        result = recommendation_engine.explain_course("Python", "Data Scientist")
        assert "Data Scientist" in result  # fallback message mentions the goal


class TestPeopleLikeYou:
    def test_no_peers_returns_empty(self, db_session):
        """With only one learner, there are no peers to aggregate."""
        profile = models.LearnerProfile(interests=["python_basics"], domain="Data Science")
        db_session.add(profile)
        db_session.commit()
        result = recommendation_engine.people_like_you_studied(profile, db_session)
        assert result == []

    def test_returns_courses_from_overlapping_peers(self, db_session):
        """A peer with a shared interest + a learning path should surface its courses."""
        me = models.LearnerProfile(interests=["python_basics"], domain="Data Science")
        db_session.add(me)
        peer = models.LearnerProfile(interests=["python_basics"], domain="Data Science")
        db_session.add(peer)
        db_session.commit()
        peer_path = models.LearningPath(
            learner_id=peer.id,
            ordered_nodes=[
                {"skill_id": "python_basics", "course_id": "python_basics", "status": "current"},
                {"skill_id": "statistics", "course_id": "statistics", "status": "locked"},
            ],
        )
        db_session.add(peer_path)
        db_session.commit()
        result = recommendation_engine.people_like_you_studied(me, db_session, limit=5)
        ids = [r["id"] for r in result]
        assert "python_basics" in ids
        assert "statistics" in ids
