import sys

import pytest


def test_health():
    if sys.version_info >= (3, 12):
        pytest.skip("FastAPI/Pydantic pins target Python 3.6 and do not import on Python 3.12")

    from fastapi.testclient import TestClient

    from app.main import app

    client = TestClient(app)
    response = client.get("/api/v1/health")

    assert response.status_code == 200
    assert response.json()["status"] == "ok"
