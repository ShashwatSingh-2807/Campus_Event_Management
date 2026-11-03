"""Tests for process liveness and dependency readiness endpoints."""

from collections.abc import Generator

from fastapi.testclient import TestClient
from sqlalchemy.exc import SQLAlchemyError

from app.db.session import get_db
from app.main import app


class HealthyFakeSession:
    def execute(self, _statement: object) -> int:
        return 1

    def close(self) -> None:
        pass


class UnavailableFakeSession:
    def execute(self, _statement: object) -> None:
        raise SQLAlchemyError("database unavailable")

    def close(self) -> None:
        pass


def override_db(session: object):
    def dependency() -> Generator[object, None, None]:
        yield session

    return dependency


def test_liveness_does_not_require_database() -> None:
    with TestClient(app) as client:
        response = client.get("/health/live")

    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_readiness_succeeds_when_database_is_available() -> None:
    app.dependency_overrides[get_db] = override_db(HealthyFakeSession())
    try:
        with TestClient(app) as client:
            response = client.get("/health/ready")
    finally:
        app.dependency_overrides.clear()

    assert response.status_code == 200
    assert response.json() == {
        "status": "ready",
        "dependencies": {"database": "ok"},
    }


def test_readiness_returns_503_when_database_is_unavailable() -> None:
    app.dependency_overrides[get_db] = override_db(UnavailableFakeSession())
    try:
        with TestClient(app) as client:
            response = client.get("/health/ready")
    finally:
        app.dependency_overrides.clear()

    assert response.status_code == 503
    assert response.json()["status"] == "not_ready"
