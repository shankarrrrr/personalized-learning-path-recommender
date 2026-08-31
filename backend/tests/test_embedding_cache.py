"""Regression tests for the embedding cache detachment bug.

The embedding service caches course data so recommendation lookups don't
re-query the DB on every skill. Originally it cached the ORM objects
themselves, which are bound to the session that loaded them. Once that
request's session closed, any later access to an expired attribute (e.g.
``course.skills_taught``) raised ``DetachedInstanceError`` and produced a
500 on ``/path/generate`` and the ``/progress/update`` skip flow.

These tests pin the fix: the cache must hold session-independent snapshots
that stay readable after the originating session is gone.
"""
import types as _types

import pytest

import models
from services import embedding_service
from services.recommendation_service import recommendation_service


def _build_two_courses(session):
    """Insert courses with IDs distinct from conftest's seeded set."""
    session.add_all([
        models.Course(
            id="python_advanced_cache_test",
            title="Python Advanced",
            description="Advanced Python.",
            domain="Data Science",
            skills_taught=["python_advanced"],
            prerequisites=[],
            level="Intermediate",
            format="Video",
            duration="6 weeks",
            embedding_vector=[0.3] * 8,
        ),
        models.Course(
            id="sql_advanced_cache_test",
            title="SQL Advanced",
            description="Advanced SQL.",
            domain="Data Science",
            skills_taught=["sql_advanced"],
            prerequisites=[],
            level="Intermediate",
            format="Interactive",
            duration="6 weeks",
            embedding_vector=[0.4] * 8,
        ),
    ])
    session.commit()


class TestCourseSnapshotIsSessionIndependent:
    """The cached course objects must outlive their originating session."""

    def test_snapshot_returns_simple_namespace(self, db_session):
        """Snapshots must support attribute access (no ORM lazy loading)."""
        _build_two_courses(db_session)
        embedding_service.embedding_service.build_course_index(db_session)
        courses = embedding_service.embedding_service.get_cached_courses(db_session)
        assert courses  # non-empty
        # Every cached entry must be a SimpleNamespace (not an ORM Course).
        for c in courses:
            assert isinstance(c, _types.SimpleNamespace)
            # Attribute access works without an active session.
            assert isinstance(c.id, str)
            assert isinstance(c.skills_taught, list)

    def test_retrieve_best_course_across_two_sessions(self, db_session, monkeypatch):
        """Reproduce the original DetachedInstanceError: build the index in
        one session, close it, then retrieve_best_course in a fresh session.

        Before the fix this raised DetachedInstanceError on the detached
        cached Course object. After the fix it returns a course snapshot
        whose attributes are fully readable.
        """
        _build_two_courses(db_session)

        # Avoid real Gemini calls: stub the query embedding to a deterministic
        # vector so the similarity step never hits the network. Use an 8-dim
        # vector to match the 8-dim course vectors in the seeded/conftest data.
        emb_svc = embedding_service.embedding_service
        monkeypatch.setattr(emb_svc, "embedding_dim", 8)
        monkeypatch.setattr(
            emb_svc, "get_embedding",
            lambda text: [0.3] * 8,
        )
        monkeypatch.setattr(emb_svc, "client", object())  # truthy so no zero-vector fallback

        # Build the cache under the first session.
        emb_svc.build_course_index(db_session)
        # Simulate a request ending: expire+close the original session so the
        # cached ORM objects (had we cached them) would be detached.
        db_session.expire_all()
        db_session.close()

        # A second, independent session for the "next request".
        engine = db_session.bind
        from sqlalchemy.orm import sessionmaker
        NewSession = sessionmaker(bind=engine, autoflush=False, autocommit=False)
        new_session = NewSession()

        try:
            profile = models.LearnerProfile(
                goal="Data Scientist",
                current_level="Beginner",
                preferred_format="Video",
                known_skills=[],
            )
            new_session.add(profile)
            new_session.commit()
            new_session.refresh(profile)

            # This used to raise DetachedInstanceError when iterating cached
            # Course objects and reading c.skills_taught.
            course = recommendation_service.retrieve_best_course(
                "python_advanced", new_session, profile,
            )
            assert course is not None
            # Reading attributes must not raise even though the course came
            # from the cross-session cache. Before the fix, this is where the
            # DetachedInstanceError surfaced (reading c.skills_taught on a
            # detached ORM object).
            assert isinstance(course.id, str)
            assert isinstance(course.skills_taught, list)
            assert isinstance(course.title, str)
            assert isinstance(course.level, str)
        finally:
            new_session.close()
            # Reset the singleton cache so it doesn't leak into other tests.
            emb_svc.course_index = {}
            emb_svc._cached_courses = None
            emb_svc.is_initialized = False
            emb_svc._query_cache = {}
