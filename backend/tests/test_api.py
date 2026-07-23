import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_health_check():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok", "service": "TrialSense AI Backend"}

# More comprehensive tests would mock the DB and test CRUD operations
# def test_create_patient(mock_db):
#     ...
