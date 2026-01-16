from fastapi.testclient import TestClient

from app import app

client = TestClient(app)


def test_health_endpoint_exists():
    """
    Test bahwa endpoint /health bisa diakses
    """
    response = client.get("/health")

    assert response.status_code == 200


def test_health_response_structure():
    """
    Test struktur response health
    """
    response = client.get("/health")
    data = response.json()

    # Field utama
    assert "status" in data
    assert "service" in data
    assert "version" in data
    assert "uptime_seconds" in data
    assert "models" in data
    assert "device" in data


def test_health_status_ok():
    """
    Test status health harus 'ok'
    """
    response = client.get("/health")
    data = response.json()

    assert data["status"] == "ok"


def test_health_model_status():
    """
    Test status model CLIP & CNN
    """
    response = client.get("/health")
    data = response.json()

    assert "clip" in data["models"]
    assert "cnn" in data["models"]

    assert data["models"]["clip"] in ["loaded", "not_loaded"]
    assert data["models"]["cnn"] in ["loaded", "not_loaded"]


def test_health_uptime_is_integer():
    """
    Test uptime adalah integer >= 0
    """
    response = client.get("/health")
    data = response.json()

    assert isinstance(data["uptime_seconds"], int)
    assert data["uptime_seconds"] >= 0
