"""
Pytest configuration and shared fixtures for the backend test suite.

Uses an in-memory SQLite database so tests are isolated and fast. AI/embedding
calls are mocked so the suite runs offline and without consuming Gemini quota.
"""
import os
import sys
from pathlib import Path

# Make the backend directory importable.
BACKEND_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(BACKEND_DIR))

import pytest
import httpx
import asyncio
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

# Point at a dummy key before importing so services don't try real config.
os.environ.setdefault("GEMINI_API_KEY", "test-key-not-used")
os.environ.setdefault("JWT_SECRET_KEY", "test-secret-key-for-pytest")

import main as app_module  # noqa: E402
import models  # noqa: E402
from database import Base  # noqa: E402
from services.cache import response_cache  # noqa: E402
import auth_deps  # noqa: E402

# IMPORTANT: endpoints in main.py depend on main.get_db, while the auth
# dependencies (get_current_user/get_current_user_optional) depend on
# auth_deps.get_db. Dependency overrides are keyed by function identity, so
# we must override both function objects.
_ENDPOINT_GET_DB = app_module.get_db
_AUTH_GET_DB = auth_deps.get_db


@pytest.fixture(autouse=True)
def _clear_response_cache():
    """Clear the module-level response cache between tests so cached values
    from one test (or a prior 404) don't leak into another."""
    response_cache.clear()
    yield
    response_cache.clear()


@pytest.fixture(scope="function")
def db_session():
    """Provide a fresh in-memory SQLite session for each test (full isolation)."""
    engine = create_engine(
        "sqlite://",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    Base.metadata.create_all(bind=engine)
    TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    session = TestingSessionLocal()

    # Seed a small set of courses + careers so endpoints have data.
    _seed_minimal_data(session)

    yield session

    session.close()
    Base.metadata.drop_all(bind=engine)


@pytest.fixture(scope="function")
def client(db_session):
    """httpx client wired to the ASGI app + in-memory test database.

    Uses httpx.ASGITransport directly (FastAPI's TestClient is incompatible
    with the installed httpx 0.28 which dropped the `app=` constructor arg).
    """
    def _override_get_db():
        try:
            yield db_session
        finally:
            pass

    app_module.app.dependency_overrides[_ENDPOINT_GET_DB] = _override_get_db
    app_module.app.dependency_overrides[_AUTH_GET_DB] = _override_get_db
    # httpx 0.28 + starlette 0.27 version mismatch makes FastAPI's TestClient
    # unusable. Use an async httpx.AsyncClient over ASGITransport and run each
    # request through a sync wrapper so tests stay synchronous.
    transport = httpx.ASGITransport(app=app_module.app)
    client = _SyncASGIClient(transport)
    yield client
    app_module.app.dependency_overrides.clear()
    app_module.app.dependency_overrides.pop(_ENDPOINT_GET_DB, None)
    app_module.app.dependency_overrides.pop(_AUTH_GET_DB, None)


class _SyncASGIClient:
    """Synchronous wrapper around an httpx.AsyncClient+ASGITransport.

    Exposes the subset of httpx.Client methods the tests use (get/post/put/
    patch/delete) so test code reads like a normal sync client.
    """

    def __init__(self, transport):
        self._transport = transport

    def _run(self, coro):
        return asyncio.get_event_loop().run_until_complete(coro)

    async def _request(self, method, path, **kwargs):
        async with httpx.AsyncClient(transport=self._transport, base_url="http://testserver") as ac:
            return await ac.request(method, path, **kwargs)

    def request(self, method, path, **kwargs):
        return self._run(self._request(method, path, **kwargs))

    def get(self, path, **kwargs):
        return self.request("GET", path, **kwargs)

    def post(self, path, **kwargs):
        return self.request("POST", path, **kwargs)

    def put(self, path, **kwargs):
        return self.request("PUT", path, **kwargs)

    def patch(self, path, **kwargs):
        return self.request("PATCH", path, **kwargs)

    def delete(self, path, **kwargs):
        return self.request("DELETE", path, **kwargs)


def _seed_minimal_data(session):
    """Insert a minimal but realistic set of courses and a career."""
    courses = [
        models.Course(
            id="python_basics",
            title="Python for Everybody",
            description="Fundamental programming concepts in Python.",
            domain="Data Science",
            skills_taught=["python_basics"],
            prerequisites=[],
            level="Beginner",
            format="Video",
            duration="6 weeks",
            platform="Coursera",
            course_url="https://example.com/python",
            instructor="UMich",
            rating=4.8,
            rating_count=1000,
            price="Subscription",
            is_free=False,
            embedding_vector=[0.1] * 8,
        ),
        models.Course(
            id="statistics",
            title="Statistics and Probability",
            description="Descriptive and inferential statistics.",
            domain="Data Science",
            skills_taught=["statistics"],
            prerequisites=[],
            level="Beginner",
            format="Interactive",
            duration="6 weeks",
            platform="Khan Academy",
            course_url="https://example.com/stats",
            instructor="Khan",
            rating=4.8,
            rating_count=2000,
            price="Free",
            is_free=True,
            embedding_vector=[0.2] * 8,
        ),
        models.Course(
            id="machine_learning",
            title="Machine Learning Specialization",
            description="Supervised and unsupervised learning.",
            domain="Data Science",
            skills_taught=["machine_learning"],
            prerequisites=["python_basics", "statistics"],
            level="Advanced",
            format="Video",
            duration="3 months",
            platform="Coursera",
            course_url="https://example.com/ml",
            instructor="Stanford",
            rating=4.9,
            rating_count=20000,
            price="Subscription",
            is_free=False,
            embedding_vector=[0.3] * 8,
        ),
    ]
    for c in courses:
        session.add(c)

    career = models.CareerPath(
        id="data_scientist",
        title="Data Scientist",
        description="Analyze datasets to extract insights.",
        domain="Data Science",
        avg_salary_min=95000,
        avg_salary_max=165000,
        job_growth="+22%",
        demand_level="High",
        required_skills=["python_basics", "statistics", "machine_learning"],
        optional_skills=["sql_basics"],
        estimated_time_months=8,
        difficulty_level="Advanced",
        typical_job_titles=["Data Scientist"],
        industries=["Technology"],
        remote_friendly="Yes",
        learning_objectives=["Build ML models"],
        career_progression=["DS -> Senior DS"],
    )
    session.add(career)
    session.commit()
