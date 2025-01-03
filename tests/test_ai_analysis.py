import pytest
from fastapi.testclient import TestClient
from app.main import app

def test_analyze_text(auth_client):
    response = auth_client.post(
        "/api/v1/ai/analyze",
        json={
            "text": "Paciente apresenta sintomas de ansiedade e insônia"
        }
    )
    assert response.status_code == 200
    data = response.json()
    assert "diagnosticos" in data
    assert "entidades" in data
    assert "recomendacoes" in data