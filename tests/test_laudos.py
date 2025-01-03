import pytest
from fastapi.testclient import TestClient
from app.main import app


@pytest.fixture
def auth_client(client):
    # Criar usuário e fazer login
    client.post(
        "/api/v1/auth/register",
        json={
            "nome": "Test User",
            "email": "test@example.com",
            "senha": "testpass123",
            "crp": "12345"
        }
    )

    response = client.post(
        "/api/v1/auth/login",
        data={
            "username": "test@example.com",
            "password": "testpass123"
        }
    )

    token = response.json()["access_token"]
    client.headers = {
        "Authorization": f"Bearer {token}"
    }
    return client


def test_create_laudo(auth_client):
    response = auth_client.post(
        "/api/v1/laudos/",
        json={
            "paciente_nome": "João Silva",
            "diagnostico": "Diagnóstico teste"
        }
    )
    assert response.status_code == 200
    data = response.json()
    assert data["paciente_nome"] == "João Silva"
    assert "id" in data


def test_list_laudos(auth_client):
    # Criar um laudo primeiro
    auth_client.post(
        "/api/v1/laudos/",
        json={
            "paciente_nome": "João Silva",
            "diagnostico": "Diagnóstico teste"
        }
    )

    response = auth_client.get("/api/v1/laudos/")
    assert response.status_code == 200
    data = response.json()
    assert len(data) > 0
    assert data[0]["paciente_nome"] == "João Silva"
