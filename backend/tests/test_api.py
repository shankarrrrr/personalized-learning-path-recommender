"""Tests for the public API endpoints (health, careers, courses)."""
import pytest


class TestHealth:
    def test_health_ok(self, client):
        r = client.get("/health")
        assert r.status_code == 200
        body = r.json()
        assert body["status"] == "ok"
        assert "ai_service" in body
        assert "db" in body
        assert "courses" in body


class TestCareers:
    def test_list_careers(self, client):
        r = client.get("/careers")
        assert r.status_code == 200
        careers = r.json()
        assert len(careers) >= 1
        assert careers[0]["id"] == "data_scientist"

    def test_get_career_by_id(self, client):
        r = client.get("/careers/data_scientist")
        assert r.status_code == 200
        assert r.json()["title"] == "Data Scientist"

    def test_get_career_not_found(self, client):
        r = client.get("/careers/does_not_exist")
        assert r.status_code == 404

    def test_career_domains(self, client):
        r = client.get("/careers/domains/list")
        assert r.status_code == 200
        assert "Data Science" in r.json()["domains"]

    def test_career_stats(self, client):
        r = client.get("/careers/stats/summary")
        assert r.status_code == 200
        body = r.json()
        assert body["total_career_paths"] >= 1
        assert "salary_range" in body

    def test_career_stats_cached_second_call(self, client):
        """Second call should be served from the response cache."""
        r1 = client.get("/careers/stats/summary")
        r2 = client.get("/careers/stats/summary")
        assert r1.status_code == 200 and r2.status_code == 200
        assert r1.json() == r2.json()


class TestCourses:
    def test_get_course_by_id(self, client):
        r = client.get("/courses/python_basics")
        assert r.status_code == 200
        body = r.json()
        assert body["title"] == "Python for Everybody"
        assert body["platform"] == "Coursera"
        assert body["is_free"] is False

    def test_get_course_not_found(self, client):
        r = client.get("/courses/nope")
        assert r.status_code == 404

    def test_course_response_cached(self, client):
        r1 = client.get("/courses/python_basics")
        r2 = client.get("/courses/python_basics")
        assert r1.json() == r2.json()


class TestErrorHandling:
    def test_validation_error_shape(self, client):
        """Onboarding with no body should return a structured 422 error."""
        r = client.post("/onboard", json={})
        assert r.status_code == 422
        body = r.json()
        assert "error" in body
        assert body["error"] == "validation_error"
        assert "message" in body
        assert "detail" in body

    def test_profile_not_found(self, client):
        r = client.get("/profile/999999")
        assert r.status_code == 404
