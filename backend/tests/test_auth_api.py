"""Tests for the auth API endpoints (register/login/me)."""
import pytest

from services.auth_service import decode_access_token


class TestRegister:
    def test_register_success(self, client):
        r = client.post("/auth/register", json={
            "email": "new@example.com",
            "username": "newuser",
            "password": "password123",
        })
        assert r.status_code == 200
        body = r.json()
        assert body["token_type"] == "bearer"
        assert "access_token" in body
        assert body["user"]["email"] == "new@example.com"
        # The token should decode to the new user id.
        payload = decode_access_token(body["access_token"])
        assert payload is not None
        assert payload["sub"] == str(body["user"]["id"])

    def test_register_duplicate_email_conflict(self, client):
        payload = {"email": "dup@example.com", "username": "dup1", "password": "password123"}
        client.post("/auth/register", json=payload)
        payload["username"] = "dup2"  # same email, different username
        r = client.post("/auth/register", json=payload)
        assert r.status_code == 409

    def test_register_short_password_rejected(self, client):
        r = client.post("/auth/register", json={
            "email": "x@example.com", "username": "short", "password": "123",
        })
        assert r.status_code == 422

    def test_register_invalid_email_rejected(self, client):
        r = client.post("/auth/register", json={
            "email": "not-an-email", "username": "bademail", "password": "password123",
        })
        assert r.status_code == 422


class TestLogin:
    def test_login_success(self, client):
        client.post("/auth/register", json={
            "email": "login@example.com", "username": "loginer", "password": "password123",
        })
        r = client.post("/auth/login", json={
            "email": "login@example.com", "password": "password123",
        })
        assert r.status_code == 200
        assert "access_token" in r.json()

    def test_login_wrong_password(self, client):
        client.post("/auth/register", json={
            "email": "wp@example.com", "username": "wper", "password": "password123",
        })
        r = client.post("/auth/login", json={
            "email": "wp@example.com", "password": "wrongpass",
        })
        assert r.status_code == 401

    def test_login_unknown_user(self, client):
        r = client.post("/auth/login", json={
            "email": "ghost@example.com", "password": "password123",
        })
        assert r.status_code == 401


class TestMe:
    def _auth_headers(self, client, email="me@example.com", username="mer", password="password123"):
        r = client.post("/auth/register", json={"email": email, "username": username, "password": password})
        token = r.json()["access_token"]
        return {"Authorization": f"Bearer {token}"}

    def test_me_with_valid_token(self, client):
        headers = self._auth_headers(client)
        r = client.get("/auth/me", headers=headers)
        assert r.status_code == 200
        assert r.json()["username"] == "mer"

    def test_me_without_token(self, client):
        r = client.get("/auth/me")
        assert r.status_code == 401

    def test_me_with_invalid_token(self, client):
        r = client.get("/auth/me", headers={"Authorization": "Bearer not.a.token"})
        assert r.status_code == 401
