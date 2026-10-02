from datetime import datetime, timedelta

def test_root_health_check(client):
    response = client.get("/")
    assert response.status_code == 200
    assert response.json()["status"] == "online"

def test_criar_usuario_e_login(client):
    # Criar admin
    payload = {
        "nome": "Admin Teste",
        "email": "admin@test.com",
        "senha": "password123",
        "perfil": "admin"
    }
    resp = client.post("/api/v1/usuarios", json=payload)
    assert resp.status_code == 201
    assert resp.json()["email"] == "admin@test.com"

    # Login
    login_data = {"username": "admin@test.com", "password": "password123"}
    resp_login = client.post("/api/v1/auth/login", data=login_data)
    assert resp_login.status_code == 200
    assert "access_token" in resp_login.json()

def test_rn01_email_duplicado(client):
    payload = {
        "nome": "Outro Admin",
        "email": "admin@test.com",
        "senha": "password123",
        "perfil": "admin"
    }
    resp = client.post("/api/v1/usuarios", json=payload)
    assert resp.status_code == 400
    assert "Já existe uma conta" in resp.json()["detail"]

def test_rn03_data_inicio_passada(client):
    # Login para obter token
    login_data = {"username": "admin@test.com", "password": "password123"}
    token = client.post("/api/v1/auth/login", data=login_data).json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    evento_invalido = {
        "nome": "Evento Antigo",
        "descricao": "Teste de data no passado",
        "local": "Auditório A",
        "data_inicio": (datetime.now() - timedelta(days=2)).isoformat(),
        "data_fim": (datetime.now() - timedelta(days=1)).isoformat(),
        "capacidade": 100
    }
    resp = client.post("/api/v1/eventos", json=evento_invalido, headers=headers)
    assert resp.status_code == 400
    assert "passado" in resp.json()["detail"]
